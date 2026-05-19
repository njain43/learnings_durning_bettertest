"""
Unit tests for FIX 4.2 Encoder
"""

import unittest
import logging
from src.fix42.encoder import FIX42Encoder
from src.fix42.message import SOH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestFIX42Encoder(unittest.TestCase):
    """Test cases for FIX 4.2 Encoder"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests"""
        cls.encoder = FIX42Encoder()

    def setUp(self):
        """Reset encoder before each test"""
        self.encoder = FIX42Encoder()

    def test_encoder_init(self):
        """Test encoder initialization"""
        encoder = FIX42Encoder()
        self.assertEqual(encoder.begin_string, 'FIX.4.2')

    def test_encoder_init_custom_begin_string(self):
        """Test encoder initialization with custom begin string"""
        encoder = FIX42Encoder(begin_string='FIX.4.1')
        self.assertEqual(encoder.begin_string, 'FIX.4.1')

    def test_simple_message_encoding(self):
        """Test encoding a simple FIX message"""
        fields = {
            '35': 'A',  # MsgType: Logon
            '49': 'SENDER',
            '56': 'TARGET',
        }
        
        encoded = self.encoder.encode(fields)
        
        logger.info(f"Input fields: {fields}")
        logger.info(f"Encoded message (hex): {encoded.hex()}")
        logger.info(f"Encoded message (repr): {repr(encoded)}")
        logger.info(f"Encoded message size: {len(encoded)} bytes")
        logger.info(f"pipe separeter: {self.encoder.get_formatted_message()}")
        # Verify it returns bytes
        self.assertIsInstance(encoded, bytes)
        
        # Verify message contains BeginString
        self.assertIn(b'8=FIX.4.2', encoded)
        
        # Verify message contains BodyLength
        self.assertIn(b'9=', encoded)
        
        # Verify message contains checksum
        self.assertIn(b'10=', encoded)

    def test_message_contains_soh_separator(self):
        """Test that encoded message uses SOH as separator"""
        fields = {
            '35': 'D',  # NewOrderSingle
            '49': 'SENDER',
        }

        encoded = self.encoder.encode(fields)

        # Verify SOH is present
        self.assertIn(SOH.encode('utf-8'), encoded)

    def test_checksum_calculation(self):
        """Test checksum calculation"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
        }

        encoded = self.encoder.encode(fields)
        encoded_str = encoded.decode('utf-8')

        # Extract checksum
        parts = encoded_str.split(SOH)
        checksum_field = [p for p in parts if p.startswith('10=')]

        self.assertTrue(len(checksum_field) > 0)
        tag, value = checksum_field[0].split('=')

        # Checksum should be 3 digits
        self.assertEqual(len(value), 3)
        self.assertTrue(value.isdigit())

    def test_body_length_calculation(self):
        """Test BodyLength field calculation"""
        fields = {
            '35': 'D',
            '49': 'SENDER',
            '56': 'TARGET',
            '34': '1',
        }

        encoded = self.encoder.encode(fields)
        encoded_str = encoded.decode('utf-8')

        # Extract BodyLength
        parts = encoded_str.split(SOH)
        body_length_field = [p for p in parts if p.startswith('9=')]

        self.assertTrue(len(body_length_field) > 0)
        tag, value = body_length_field[0].split('=')

        # BodyLength should be numeric
        self.assertTrue(value.isdigit())
        self.assertGreater(int(value), 0)

    def test_new_order_single_message(self):
        """Test encoding a NewOrderSingle message"""
        fields = {
            '35': 'D',           # MsgType: NewOrderSingle
            '49': 'SENDER',      # SenderCompID
            '56': 'TARGET',      # TargetCompID
            '34': '1',           # MsgSeqNum
            '52': '20240519-10:30:00',  # SendingTime
            '55': 'MSFT',        # Symbol
            '54': '1',           # Side: Buy
            '38': '100',         # OrderQty
            '40': '2',           # OrdType: Limit
            '44': '150.50',      # Price
        }
        
        encoded = self.encoder.encode(fields)
        
        logger.info(f"NewOrderSingle - Input fields: {fields}")
        logger.info(f"NewOrderSingle - Encoded message (hex): {encoded.hex()}")
        logger.info(f"NewOrderSingle - Encoded message (repr): {repr(encoded)}")
        logger.info(f"NewOrderSingle - Encoded message size: {len(encoded)} bytes")
        
        self.assertIsInstance(encoded, bytes)
        self.assertIn(b'35=D', encoded)  # Message type
        self.assertIn(b'55=MSFT', encoded)  # Symbol
        self.assertIn(b'44=150.50', encoded)  # Price

    def test_value_method_returns_encoded_message(self):
        """Test that value() method returns the encoded message"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
        }

        encoded = self.encoder.encode(fields)
        value = self.encoder.value()

        self.assertEqual(encoded, value)

    def test_special_characters_in_values(self):
        """Test encoding with special characters in field values"""
        fields = {
            '35': 'D',
            '49': 'SENDER-TEST',
            '56': 'TARGET_TEST',
            '58': 'Order for client@example.com',
        }

        encoded = self.encoder.encode(fields)

        self.assertIsInstance(encoded, bytes)
        self.assertIn(b'49=SENDER-TEST', encoded)
        self.assertIn(b'56=TARGET_TEST', encoded)

    def test_numeric_values_as_strings(self):
        """Test that numeric field values are properly handled as strings"""
        fields = {
            '35': 'D',
            '38': '1000',  # OrderQty
            '44': '99.99',  # Price
        }

        encoded = self.encoder.encode(fields)

        self.assertIn(b'38=1000', encoded)
        self.assertIn(b'44=99.99', encoded)

    def test_field_ordering_consistency(self):
        """Test that fields are ordered consistently"""
        fields = {
            '56': 'TARGET',
            '49': 'SENDER',
            '35': 'A',
        }

        encoded1 = self.encoder.encode(fields)

        self.encoder = FIX42Encoder()  # Reset
        encoded2 = self.encoder.encode(fields)

        # Should produce identical results
        self.assertEqual(encoded1, encoded2)

    def test_empty_message_encoding(self):
        """Test encoding a message with only MsgType"""
        fields = {'35': 'A'}

        encoded = self.encoder.encode(fields)

        self.assertIsInstance(encoded, bytes)
        self.assertIn(b'35=A', encoded)
        self.assertIn(b'10=', encoded)  # Checksum


if __name__ == '__main__':
    unittest.main()

