import unittest
import threading
import logging

from src.network.tcp.server import TCPServer
from src.network.tcp.client import TCPClient


# Configure root logger for tests so we can see debug output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s')


class TestTCPServerClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # start echo server
        cls.server = TCPServer()
        cls.server.start()
        cls.host = cls.server.host
        cls.port = cls.server.port

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_echo(self):
        client = TCPClient(self.host, self.port)
        resp = client.send(b"hello")
        self.assertEqual(resp, b"hello")

    def test_multiple_clients(self):
        results = []

        def worker(msg, idx):
            c = TCPClient(self.host, self.port)
            r = c.send(msg)
            results.append((idx, r))

        threads = []
        for i in range(5):
            t = threading.Thread(target=worker, args=(f"msg-{i}".encode(), i))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # sort by index and validate responses
        results.sort()
        for i, r in results:
            self.assertEqual(r, f"msg-{i}".encode())

    def test_stop_server_rejects(self):
        # stop server and ensure new connections are refused
        self.server.stop()
        c = TCPClient(self.host, self.port)
        with self.assertRaises(Exception):
            c.send(b"after-stop")
        # restart server for other tests if needed
        self.server.start()


if __name__ == "__main__":
    unittest.main()
