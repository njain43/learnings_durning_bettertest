import unittest
import logging

from src.network.tcp.server import TCPServer
from src.network.tcp.client import TCPClient
from src.fix42.encoder import FIX42Encoder
from src.fix42.decoder import FIX42Decoder


# Configure logging for this test module so FIX messages and TCP events are visible
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)


class TestFIXOverTCP(unittest.TestCase):
    def test_logon_and_neworder_executionreport(self):
        """Start a TCP-based FIX server, send Logon then NewOrderSingle and expect ExecutionReport."""

        # Handler that accepts Logon and responds to NewOrderSingle with ExecutionReport
        def fix_handler(conn, addr, data: bytes) -> bytes:
            decoder = FIX42Decoder()
            decoded = decoder.decode(data)
            msg_type = decoded.get('35')

            logger.debug("Handler received message from %s: %s", addr, decoder.get_formatted_message())

            # On Logon, just record and do not respond (could reply with Logon ack if desired)
            if msg_type == 'A':
                return b''

            # On NewOrderSingle, respond with ExecutionReport
            if msg_type == 'D':
                clordid = decoded.get('11', '1')
                symbol = decoded.get('55', '')
                qty = decoded.get('38', '')

                exec_fields = {
                    '35': '8',  # ExecutionReport
                    '49': decoded.get('56', 'SERVER'),
                    '56': decoded.get('49', 'CLIENT'),
                    '11': clordid,
                    '17': '1',  # ExecID
                    '150': '0',  # ExecType = New
                    '39': '0',  # OrdStatus = New
                    '55': symbol,
                    '38': qty,
                }
                encoder = FIX42Encoder()
                encoded = encoder.encode(exec_fields)
                logger.debug("Handler sending ExecutionReport: %s", encoder.get_formatted_message())
                return encoded

            return b''

        server = TCPServer(handler=fix_handler)
        server.start()
        try:
            host = server.host
            port = server.port

            # Send Logon message (client -> server)
            encoder = FIX42Encoder()
            logon_fields = {'35': 'A', '49': 'CLIENT', '56': 'SERVER', '98': '0', '108': '30'}
            logon_msg = encoder.encode(logon_fields)
            logger.debug("Client will send Logon: %s", encoder.get_formatted_message())

            client = TCPClient(host, port)
            # logon_response may be empty as handler returns b'' for logon
            logon_response = client.send(logon_msg)
            logger.debug("Client received Logon response (raw): %r", logon_response)
            self.assertTrue(isinstance(logon_response, (bytes, bytearray)))

            # Now send NewOrderSingle
            new_order_fields = {'35': 'D', '49': 'CLIENT', '56': 'SERVER', '11': 'ORD-1', '55': 'AAPL', '54': '1', '38': '100'}
            new_order_msg = encoder.encode(new_order_fields)
            logger.debug("Client will send NewOrderSingle: %s", encoder.get_formatted_message())

            resp = client.send(new_order_msg)
            logger.debug("Client received response (raw): %r", resp)
            self.assertTrue(resp)

            # Decode response and assert it is ExecutionReport
            decoder = FIX42Decoder()
            decoded = decoder.decode(resp)
            logger.debug("Client decoded response: %s", decoder.get_formatted_message())
            self.assertEqual(decoded.get('35'), '8')
            self.assertEqual(decoded.get('11'), 'ORD-1')
            self.assertEqual(decoded.get('150'), '0')
            self.assertEqual(decoded.get('39'), '0')
            self.assertEqual(decoded.get('55'), 'AAPL')
            self.assertEqual(decoded.get('38'), '100')

        finally:
            server.stop()


if __name__ == '__main__':
    unittest.main()
