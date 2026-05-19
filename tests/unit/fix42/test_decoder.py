"""
Unit tests for FIX 4.2 Decoder
"""

import unittest
import logging
from src.fix42.encoder import FIX42Encoder
from src.fix42.decoder import FIX42Decoder
from src.fix42.message import SOH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestFIX42Decoder(unittest.TestCase):
    """Test cases for FIX 4.2 Decoder"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests"""
        cls.encoder = FIX42Encoder()
        cls.decoder = FIX42Decoder()
    
    def setUp(self):
        """Reset decoder before each test"""
        self.decoder = FIX42Decoder()
        self.encoder = FIX42Encoder()
    
    def test_decoder_init(self):
        """Test decoder initialization"""
        decoder = FIX42Decoder()
        self.assertIsNotNone(decoder)
    
    def test_simple_message_decoding(self):
        """Test decoding a simple FIX message"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
            '56': 'TARGET',
        }
        
        encoded = self.encoder.encode(fields)
        logger.info(f"Encoded message (hex): {encoded.hex()}")
        logger.info(f"Encoded message (repr): {repr(encoded)}")
        
        decoded = self.decoder.decode(encoded)
        
        logger.info(f"Original fields: {fields}")
        logger.info(f"Decoded fields: {decoded}")
        
        self.assertIsInstance(decoded, dict)
        self.assertEqual(decoded['35'], 'A')
        self.assertEqual(decoded['49'], 'SENDER')
        self.assertEqual(decoded['56'], 'TARGET')
    
    def test_decode_from_string(self):
        """Test decoding from string instead of bytes"""
        fields = {
            '35': 'D',
            '49': 'SENDER',
        }
        
        encoded = self.encoder.encode(fields)
        encoded_str = encoded.decode('utf-8')
        
        decoded = self.decoder.decode(encoded_str)
        
        self.assertEqual(decoded['35'], 'D')
        self.assertEqual(decoded['49'], 'SENDER')
    
    def test_decode_contains_begin_string(self):
        """Test that decoded message contains BeginString"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
        }
        
        encoded = self.encoder.encode(fields)
        decoded = self.decoder.decode(encoded)
        
        self.assertIn('8', decoded)
        self.assertEqual(decoded['8'], 'FIX.4.2')
    
    def test_decode_contains_body_length(self):
        """Test that decoded message contains BodyLength"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
        }
        
        encoded = self.encoder.encode(fields)
        decoded = self.decoder.decode(encoded)
        
        self.assertIn('9', decoded)
        self.assertTrue(decoded['9'].isdigit())
    
    def test_decode_contains_checksum(self):
        """Test that decoded message contains CheckSum"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
        }
        
        encoded = self.encoder.encode(fields)
        decoded = self.decoder.decode(encoded)
        
        self.assertIn('10', decoded)
        self.assertEqual(len(decoded['10']), 3)
    
    def test_new_order_single_decode(self):
        """Test decoding a NewOrderSingle message"""
        fields = {
            '35': 'D',
            '49': 'SENDER',
            '56': 'TARGET',
            '34': '1',
            '55': 'MSFT',
            '54': '1',
            '38': '100',
            '40': '2',
            '44': '150.50',
        }
        
        encoded = self.encoder.encode(fields)
        logger.info(f"NewOrderSingle - Encoded message (hex): {encoded.hex()}")
        logger.info(f"NewOrderSingle - Encoded message (repr): {repr(encoded)}")
        
        decoded = self.decoder.decode(encoded)
        
        logger.info(f"NewOrderSingle - Original fields: {fields}")
        logger.info(f"NewOrderSingle - Decoded fields: {decoded}")
        
        self.assertEqual(decoded['35'], 'D')
        self.assertEqual(decoded['55'], 'MSFT')
        self.assertEqual(decoded['38'], '100')
        self.assertEqual(decoded['44'], '150.50')
    
    def test_get_field_method(self):
        """Test get_field method for retrieving specific fields"""
        fields = {
            '35': 'D',
            '49': 'SENDER',
            '55': 'MSFT',
        }
        
        encoded = self.encoder.encode(fields)
        self.decoder.decode(encoded)
        
        self.assertEqual(self.decoder.get_field('35'), 'D')
        self.assertEqual(self.decoder.get_field('49'), 'SENDER')
        self.assertEqual(self.decoder.get_field('55'), 'MSFT')
    
    def test_get_nonexistent_field(self):
        """Test get_field for non-existent field returns empty string"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
        }
        
        encoded = self.encoder.encode(fields)
        self.decoder.decode(encoded)
        
        self.assertEqual(self.decoder.get_field('999'), '')
    
    def test_value_method_returns_decoded_fields(self):
        """Test that value() method returns decoded fields"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
        }
        
        encoded = self.encoder.encode(fields)
        decoded = self.decoder.decode(encoded)
        value = self.decoder.value()
        
        self.assertEqual(value, decoded)
    
    def test_roundtrip_encoding_decoding(self):
        """Test encoding and then decoding returns original fields"""
        original_fields = {
            '35': 'D',
            '49': 'SENDER',
            '56': 'TARGET',
            '34': '5',
            '55': 'MSFT',
            '54': '2',  # Sell
            '38': '500',
            '40': '1',  # Market
            '44': '200.75',
        }
        
        # Encode
        encoded = self.encoder.encode(original_fields)
        logger.info(f"Roundtrip - Original fields: {original_fields}")
        logger.info(f"Roundtrip - Encoded message (hex): {encoded.hex()}")
        logger.info(f"Roundtrip - Encoded message (repr): {repr(encoded)}")
        logger.info(f"Roundtrip - Encoded message size: {len(encoded)} bytes")
        
        # Decode
        decoded = self.decoder.decode(encoded)
        logger.info(f"Roundtrip - Decoded fields: {decoded}")
        
        # Verify all original fields are present (plus FIX header/trailer)
        for tag, value in original_fields.items():
            self.assertEqual(decoded[tag], value)
    
    def test_checksum_verification(self):
        """Test checksum verification method"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
        }
        
        encoded = self.encoder.encode(fields)
        
        # Checksum should be valid
        self.assertTrue(self.decoder.verify_checksum(encoded))
    
    def test_checksum_verification_from_string(self):
        """Test checksum verification from string"""
        fields = {
            '35': 'D',
            '49': 'SENDER',
        }
        
        encoded = self.encoder.encode(fields)
        encoded_str = encoded.decode('utf-8')
        
        self.assertTrue(self.decoder.verify_checksum(encoded_str))
    
    def test_corrupted_checksum_fails_verification(self):
        """Test that corrupted checksum fails verification"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
        }
        
        encoded = self.encoder.encode(fields)
        encoded_str = encoded.decode('utf-8')
        
        # Corrupt the checksum
        corrupted = encoded_str.replace('10=', '10=999')
        
        self.assertFalse(self.decoder.verify_checksum(corrupted))
    
    def test_get_decoded_fields_returns_copy(self):
        """Test that get_decoded_fields returns a copy"""
        fields = {
            '35': 'A',
            '49': 'SENDER',
        }
        
        encoded = self.encoder.encode(fields)
        self.decoder.decode(encoded)
        
        decoded_copy1 = self.decoder.get_decoded_fields()
        decoded_copy2 = self.decoder.get_decoded_fields()
        
        # Should be equal
        self.assertEqual(decoded_copy1, decoded_copy2)
        
        # But modifying one shouldn't affect the other
        decoded_copy1['35'] = 'Z'
        self.assertNotEqual(decoded_copy1, decoded_copy2)
    
    def test_fixed_message_with_long_values(self):
        """Test encoding/decoding with long field values"""
        fields = {
            '35': 'D',
            '58': 'This is a longer message with multiple words and special characters!',
            '49': 'SENDER-WITH-LONG-NAME',
        }
        
        encoded = self.encoder.encode(fields)
        decoded = self.decoder.decode(encoded)
        
        self.assertEqual(decoded['58'], fields['58'])
        self.assertEqual(decoded['49'], fields['49'])


if __name__ == '__main__':
    unittest.main()

