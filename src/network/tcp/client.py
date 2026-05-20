"""Simple TCP client used in unit tests."""

import socket
import logging

logger = logging.getLogger(__name__)


class TCPClient:
    def __init__(self, host: str, port: int, timeout: float = 2.0):
        self.host = host
        self.port = port
        self.timeout = timeout

    def send(self, data: bytes) -> bytes:
        """Send data to the server and return response bytes."""
        logger.debug("Client sending %d bytes to %s:%s: %r", len(data), self.host, self.port, data)
        with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
            sock.sendall(data)
            try:
                sock.shutdown(socket.SHUT_WR)
            except Exception:
                pass

            resp = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                resp += chunk
            logger.debug("Client received %d bytes from %s:%s: %r", len(resp), self.host, self.port, resp)
            return resp
