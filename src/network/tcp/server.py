"""Robust TCP server implementation for tests and development.

This module provides a production-style TCP server implementation that uses a
ThreadPoolExecutor to handle client connections concurrently, keeps track of
active clients, and supports graceful shutdown. The default handler echoes
received bytes back to the client to preserve compatibility with existing
unit tests.

Design goals:
- Use only the Python standard library (socket, threading, concurrent.futures)
- Support multiple concurrent clients with a configurable worker pool
- Allow persistent client connections where handler is invoked for each
  incoming data chunk
- Provide clear, well-documented APIs for starting/stopping the server and
  for inspecting active connections/messages
"""

import socket
import threading
import logging
import time
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Optional, Set, Tuple, Dict

logger = logging.getLogger(__name__)


class TCPServer:
    """A robust, test-friendly TCP server.

    Parameters
    ----------
    host: str
        Address to bind the listening socket to. Defaults to '127.0.0.1'.
    port: int
        Port to bind. Use 0 to select an ephemeral port assigned by the OS.
    handler: Callable[[socket.socket, Tuple[str,int], bytes], Optional[bytes]]
        A callable invoked for each data chunk received from a client. It
        should accept (conn, addr, data) and return bytes to send back or
        None/empty to send nothing. If omitted, the server echoes received
        bytes.
    backlog: int
        Maximum backlog for the listening socket.
    max_workers: int
        Maximum number of threads to process client connections concurrently.
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 0,
        handler: Optional[Callable] = None,
        backlog: int = 100,
        max_workers: int = 10,
    ):
        # Basic configuration
        self.host = host
        self.port = port
        self.backlog = backlog
        self._handler = handler or self._default_handler

        # Internal state
        self._listen_sock: Optional[socket.socket] = None
        self._running = False
        self._accept_thread: Optional[threading.Thread] = None
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

        # Track active clients and their futures (for orderly shutdown)
        self._clients_lock = threading.Lock()
        self._client_sockets: Set[socket.socket] = set()
        self._client_futures: Dict[Future, Tuple[socket.socket, Tuple[str, int]]] = {}

        # For tests/inspection: collected messages (addr, data)
        self.received_messages = []

    # ------------------ Handler utilities ------------------
    def _default_handler(self, conn: socket.socket, addr: Tuple[str, int], data: bytes) -> Optional[bytes]:
        """Default handler: echo received bytes and record them for tests.

        This method is intentionally simple to remain compatible with existing
        test expectations (echo behaviour).
        """
        self.received_messages.append((addr, data))
        return data

    # ------------------ Lifecycle methods ------------------
    def start(self, timeout: float = 1.0) -> None:
        """Bind, listen and start the accept loop in a background thread.

        This method returns after the listening socket is established and
        ready to accept connections. If `port` was 0, the selected ephemeral
        port is assigned to `self.port`.

        timeout: float
            Maximum time (seconds) to wait for the server to become
            connectable during startup.
        """
        logger.debug("Starting TCPServer on %s:%s", self.host, self.port)
        if self._running:
            logger.debug("Server already running")
            return

        # Create, bind and listen
        self._listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._listen_sock.bind((self.host, self.port))
        self._listen_sock.listen(self.backlog)
        self._listen_sock.settimeout(0.5)  # short timeout so accept loop can check running

        # If ephemeral port chosen, update attribute
        self.port = self._listen_sock.getsockname()[1]

        self._running = True
        self._accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._accept_thread.start()

        # Wait briefly until the server is connectable
        start = time.time()
        while time.time() - start < timeout:
            try:
                with socket.create_connection((self.host, self.port), timeout=0.5):
                    break
            except Exception:
                time.sleep(0.01)

        logger.debug("TCPServer started and listening on %s:%s", self.host, self.port)

    def _accept_loop(self) -> None:
        """Accept loop that submits client handling to the thread pool.

        This runs in a dedicated background thread and will exit when
        `self._running` becomes False.
        """
        logger.debug("Accept loop running")
        while self._running:
            try:
                conn, addr = self._listen_sock.accept()
            except socket.timeout:
                continue
            except OSError:
                # listening socket closed
                break

            logger.debug("Accepted connection from %s", addr)
            # Track client socket and submit a worker
            with self._clients_lock:
                self._client_sockets.add(conn)
            fut = self._executor.submit(self._client_worker, conn, addr)
            with self._clients_lock:
                self._client_futures[fut] = (conn, addr)

            # Optionally remove finished futures to avoid memory growth
            self._cleanup_done_futures()

        logger.debug("Accept loop exiting")

    def _client_worker(self, conn: socket.socket, addr: Tuple[str, int]) -> None:
        """Handle a connected client connection.

        This method runs in a worker thread from the ThreadPoolExecutor. It
        repeatedly reads data from `conn` and invokes the configured handler
        for each non-empty chunk. If the handler returns bytes, they are
        sent back on the connection. The method returns when the client
        closes the connection or an unrecoverable error occurs.
        """
        logger.debug("Client worker started for %s", addr)
        try:
            # Set a timeout so recv doesn't block indefinitely during shutdown
            conn.settimeout(1.0)
            while self._running:
                try:
                    data = conn.recv(4096)
                except socket.timeout:
                    # timed recv; go back to check _running flag
                    continue
                except OSError:
                    break

                if not data:
                    # client closed connection
                    break

                logger.debug("Server received %d bytes from %s: %r", len(data), addr, data)
                try:
                    resp = self._handler(conn, addr, data)
                except Exception:
                    logger.exception("Handler raised for client %s", addr)
                    resp = None

                if resp:
                    try:
                        conn.sendall(resp)
                        logger.debug("Server sent %d bytes to %s", len(resp), addr)
                    except Exception:
                        logger.exception("Failed sending to client %s", addr)
                        break
        finally:
            # Cleanup client socket and record
            try:
                conn.close()
            except Exception:
                pass
            with self._clients_lock:
                if conn in self._client_sockets:
                    self._client_sockets.remove(conn)
        logger.debug("Client worker exiting for %s", addr)

    def _cleanup_done_futures(self) -> None:
        """Remove completed futures from tracking dict to prevent memory growth."""
        done = [f for f in self._client_futures.keys() if f.done()]
        for f in done:
            with self._clients_lock:
                self._client_futures.pop(f, None)

    def stop(self, wait: float = 2.0) -> None:
        """Gracefully stop the server.

        This will stop accepting new connections, close the listening socket,
        attempt to close active client sockets, and wait for worker threads
        to finish (bounded by `wait`).

        wait: float
            Maximum time in seconds to wait for worker threads to complete.
        """
        logger.debug("Stopping TCPServer on %s:%s", self.host, self.port)
        self._running = False

        # Close listening socket to unblock accept()
        if self._listen_sock:
            try:
                self._listen_sock.close()
            except Exception:
                pass
            self._listen_sock = None

        # Close all client sockets to encourage worker threads to exit
        with self._clients_lock:
            clients = list(self._client_sockets)
        for c in clients:
            try:
                c.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                c.close()
            except Exception:
                pass

        # Wait for worker threads to finish
        self._executor.shutdown(wait=False)
        # Give threads some time to finish work
        start = time.time()
        while time.time() - start < wait:
            with self._clients_lock:
                active = any(not f.done() for f in self._client_futures.keys())
            if not active:
                break
            time.sleep(0.01)

        # Forcefully shutdown executor if still pending by recreating it
        # (ThreadPoolExecutor has no direct cancel-all API). We simply replace
        # the reference so further calls after stop() start a fresh executor.
        self._executor = ThreadPoolExecutor(max_workers=self._executor._max_workers)

        logger.debug("TCPServer stopped")

    # ------------------ Inspection helpers ------------------
    def active_client_count(self) -> int:
        """Return the number of currently tracked client sockets."""
        with self._clients_lock:
            return len(self._client_sockets)

    def is_running(self) -> bool:
        """Return True if the server is currently running and accepting."""
        return self._running

