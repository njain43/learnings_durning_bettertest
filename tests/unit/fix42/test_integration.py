"""
Integration tests for FIX 4.2 Encoder/Decoder with real-world message examples
"""

import unittest
import logging
from src.fix42.encoder import FIX42Encoder
from src.fix42.decoder import FIX42Decoder
from src.fix42.message import FIXMessage, MESSAGE_TYPES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestFIX42Integration(unittest.TestCase):
    """Integration tests with real-world FIX message scenarios"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.encoder = FIX42Encoder()
        cls.decoder = FIX42Decoder()
    
    def setUp(self):
        """Reset encoder/decoder before each test"""
        self.encoder = FIX42Encoder()
        self.decoder = FIX42Decoder()
    
    def test_logon_message(self):
        """Test a Logon message exchange"""
        # Create a Logon message
        logon_fields = {
            '35': 'A',                  # MsgType: Logon
            '49': 'CLIENT1',            # SenderCompID
            '56': 'SERVER',             # TargetCompID
            '34': '1',                  # MsgSeqNum
            '52': '20240519-10:30:00',  # SendingTime
            '98': '0',                  # EncryptMethod: None
            '108': '30',                # HeartBtInt: 30 seconds
        }
        
        logger.info("="*80)
        logger.info("TEST: Logon Message")
        logger.info(f"Input fields: {logon_fields}")
        
        # Encode
        encoded = self.encoder.encode(logon_fields)
        logger.info(f"Encoded message (hex): {encoded.hex()}")
        logger.info(f"Encoded message (repr): {repr(encoded)}")
        logger.info(f"Encoded message size: {len(encoded)} bytes")
        
        # Decode
        decoded = self.decoder.decode(encoded)
        logger.info(f"Decoded fields: {decoded}")
        logger.info("="*80)
        
        # Verify
        self.assertEqual(decoded['35'], 'A')
        self.assertEqual(decoded['49'], 'CLIENT1')
        self.assertEqual(decoded['108'], '30')
    
    def test_new_order_single_buy_limit(self):
        """Test a NewOrderSingle message for a Buy Limit order"""
        order_fields = {
            '35': 'D',                      # MsgType: NewOrderSingle
            '49': 'TRADER1',                # SenderCompID
            '56': 'BROKER',                 # TargetCompID
            '34': '2',                      # MsgSeqNum
            '52': '20240519-14:30:00',      # SendingTime
            '11': 'ORDER-12345',            # ClOrdID
            '55': 'AAPL',                   # Symbol
            '54': '1',                      # Side: Buy
            '38': '1000',                   # OrderQty
            '40': '2',                      # OrdType: Limit
            '44': '180.50',                 # Price
            '59': '0',                      # TimeInForce: Day
        }
        
        logger.info("="*80)
        logger.info("TEST: NewOrderSingle - Buy Limit")
        logger.info(f"Input fields: {order_fields}")
        
        encoded = self.encoder.encode(order_fields)
        logger.info(f"Encoded message (hex): {encoded.hex()}")
        logger.info(f"Encoded message (repr): {repr(encoded)}")
        logger.info(f"Encoded message size: {len(encoded)} bytes")
        
        decoded = self.decoder.decode(encoded)
        logger.info(f"Decoded fields: {decoded}")
        logger.info("="*80)
        
        self.assertEqual(decoded['35'], 'D')
        self.assertEqual(decoded['55'], 'AAPL')
        self.assertEqual(decoded['54'], '1')  # Buy
        self.assertEqual(decoded['40'], '2')  # Limit
        self.assertEqual(decoded['44'], '180.50')
    
    def test_new_order_single_sell_market(self):
        """Test a NewOrderSingle message for a Sell Market order"""
        order_fields = {
            '35': 'D',
            '49': 'TRADER2',
            '56': 'BROKER',
            '34': '3',
            '52': '20240519-15:00:00',
            '11': 'ORDER-12346',
            '55': 'MSFT',
            '54': '2',                      # Side: Sell
            '38': '500',
            '40': '1',                      # OrdType: Market
        }
        
        encoded = self.encoder.encode(order_fields)
        decoded = self.decoder.decode(encoded)
        
        self.assertEqual(decoded['55'], 'MSFT')
        self.assertEqual(decoded['54'], '2')  # Sell
        self.assertEqual(decoded['40'], '1')  # Market
    
    def test_execution_report_filled(self):
        """Test an ExecutionReport message for a filled order"""
        exec_report = {
            '35': '8',                      # MsgType: ExecutionReport
            '49': 'BROKER',                 # SenderCompID
            '56': 'TRADER1',                # TargetCompID
            '34': '100',                    # MsgSeqNum
            '52': '20240519-14:31:00',      # SendingTime
            '37': 'EXEC-12345',             # OrderID
            '11': 'ORDER-12345',            # ClOrdID
            '150': 'F',                     # ExecType: Trade
            '39': '2',                      # OrdStatus: Filled
            '55': 'AAPL',                   # Symbol
            '54': '1',                      # Side: Buy
            '38': '1000',                   # OrderQty
            '151': '1000',                  # LeavesQty
            '14': '1000',                   # CumQty
            '6': '180.50',                  # AvgPx
        }
        
        logger.info("="*80)
        logger.info("TEST: ExecutionReport - Filled Order")
        logger.info(f"Input fields: {exec_report}")
        
        encoded = self.encoder.encode(exec_report)
        logger.info(f"Encoded message (hex): {encoded.hex()}")
        logger.info(f"Encoded message (repr): {repr(encoded)}")
        logger.info(f"Encoded message size: {len(encoded)} bytes")
        
        decoded = self.decoder.decode(encoded)
        logger.info(f"Decoded fields: {decoded}")
        logger.info("="*80)
        
        self.assertEqual(decoded['35'], '8')
        self.assertEqual(decoded['150'], 'F')  # Filled
        self.assertEqual(decoded['39'], '2')   # Filled status
        self.assertEqual(decoded['14'], '1000')  # Cum quantity
    
    def test_test_request_message(self):
        """Test a TestRequest message"""
        test_request = {
            '35': '1',                      # MsgType: TestRequest
            '49': 'CLIENT',
            '56': 'SERVER',
            '34': '10',
            '52': '20240519-16:00:00',
            '112': 'TEST-HEARTBEAT',        # TestReqID
        }
        
        encoded = self.encoder.encode(test_request)
        decoded = self.decoder.decode(encoded)
        
        self.assertEqual(decoded['35'], '1')
        self.assertEqual(decoded['112'], 'TEST-HEARTBEAT')
    
    def test_multiple_message_sequence(self):
        """Test encoding/decoding a sequence of different messages"""
        messages = [
            {'35': 'A', '49': 'CLIENT', '56': 'SERVER', '34': '1'},  # Logon
            {'35': 'D', '49': 'CLIENT', '56': 'SERVER', '34': '2', '55': 'AAPL'},  # NewOrderSingle
            {'35': '8', '49': 'SERVER', '56': 'CLIENT', '34': '1', '55': 'AAPL'},  # ExecutionReport
        ]
        
        for msg_fields in messages:
            encoded = self.encoder.encode(msg_fields)
            decoded = self.decoder.decode(encoded)
            
            # Verify all original fields are present
            for tag, value in msg_fields.items():
                self.assertEqual(decoded[tag], value)
            
            self.encoder = FIX42Encoder()  # Reset for next message
    
    def test_fix_message_builder_logon(self):
        """Test using FIXMessage builder for Logon"""
        msg = FIXMessage('A')  # Logon
        msg.add_fields({
            '49': 'CLIENT',
            '56': 'SERVER',
            '34': '1',
        })
        
        fields = msg.get_fields()
        
        logger.info("="*80)
        logger.info("TEST: FIXMessage Builder - Logon")
        logger.info(f"Built message fields: {fields}")
        
        encoded = self.encoder.encode(fields)
        logger.info(f"Encoded message (hex): {encoded.hex()}")
        logger.info(f"Encoded message (repr): {repr(encoded)}")
        
        decoded = self.decoder.decode(encoded)
        logger.info(f"Decoded fields: {decoded}")
        logger.info("="*80)
        
        self.assertEqual(decoded['35'], 'A')
        self.assertEqual(decoded['49'], 'CLIENT')
    
    def test_fix_message_builder_new_order(self):
        """Test using FIXMessage builder for NewOrderSingle"""
        msg = FIXMessage('D')  # NewOrderSingle
        msg.add_field('49', 'TRADER')
        msg.add_field('56', 'BROKER')
        msg.add_field('55', 'GOOGL')
        msg.add_field('54', '1')  # Buy
        msg.add_field('38', '100')
        msg.add_field('40', '2')  # Limit
        msg.add_field('44', '125.00')
        
        fields = msg.get_fields()
        
        logger.info("="*80)
        logger.info("TEST: FIXMessage Builder - NewOrderSingle")
        logger.info(f"Built message fields: {fields}")
        
        encoded = self.encoder.encode(fields)
        logger.info(f"Encoded message (hex): {encoded.hex()}")
        logger.info(f"Encoded message (repr): {repr(encoded)}")
        logger.info(f"Encoded message size: {len(encoded)} bytes")
        
        decoded = self.decoder.decode(encoded)
        logger.info(f"Decoded fields: {decoded}")
        logger.info("="*80)
        
        self.assertEqual(decoded['35'], 'D')
        self.assertEqual(decoded['55'], 'GOOGL')
        self.assertEqual(decoded['44'], '125.00')
    
    def test_message_with_repeating_group_simulation(self):
        """Test a message with multiple related fields (simulating repeating groups)"""
        # FIX 4.2 doesn't have true repeating groups, but we can store multiple values
        order_fields = {
            '35': 'D',
            '49': 'TRADER',
            '56': 'BROKER',
            '55': 'AAPL',
            '38': '1000',
            '40': '2',
            '44': '150.00',
            '447': 'D',                    # PartyIDSource
            '448': 'PARTY1',               # PartyID
            '447': 'D',                    # Second PartyIDSource (would override in dict)
            '449': '1',                    # PartyRole
        }
        
        encoded = self.encoder.encode(order_fields)
        decoded = self.decoder.decode(encoded)
        
        # Verify key fields
        self.assertEqual(decoded['35'], 'D')
        self.assertEqual(decoded['55'], 'AAPL')
    
    def test_large_message_encoding(self):
        """Test encoding a message with many fields"""
        large_msg = {}
        for i in range(100, 120):
            large_msg[str(i)] = f'VALUE_{i}'
        
        large_msg['35'] = 'D'  # Ensure MsgType
        
        logger.info("="*80)
        logger.info("TEST: Large Message with Many Fields")
        logger.info(f"Number of fields: {len(large_msg)}")
        logger.info(f"Input fields: {large_msg}")
        
        encoded = self.encoder.encode(large_msg)
        logger.info(f"Encoded message (hex): {encoded.hex()}")
        logger.info(f"Encoded message (repr): {repr(encoded)}")
        logger.info(f"Encoded message size: {len(encoded)} bytes")
        
        decoded = self.decoder.decode(encoded)
        logger.info(f"Decoded fields count: {len(decoded)}")
        logger.info(f"Decoded fields: {decoded}")
        logger.info(f"Checksum valid: {self.decoder.verify_checksum(encoded)}")
        logger.info("="*80)
        
        # Verify checksum is valid
        self.assertTrue(self.decoder.verify_checksum(encoded))
        
        # Verify all fields are present
        for tag, value in large_msg.items():
            self.assertEqual(decoded[tag], value)


if __name__ == '__main__':
    unittest.main()

