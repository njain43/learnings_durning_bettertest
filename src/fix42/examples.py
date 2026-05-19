"""
Sample usage examples for FIX 4.2 Encoder/Decoder
"""

from src.fix42.encoder import FIX42Encoder
from src.fix42.decoder import FIX42Decoder
from src.fix42.message import FIXMessage


def example_1_simple_encoding():
    """Example 1: Simple message encoding"""
    print("\n" + "="*60)
    print("Example 1: Simple Message Encoding")
    print("="*60)
    
    encoder = FIX42Encoder()
    
    fields = {
        '35': 'A',           # MsgType: Logon
        '49': 'CLIENT1',     # SenderCompID
        '56': 'SERVER',      # TargetCompID
        '34': '1',           # MsgSeqNum
    }
    
    encoded = encoder.encode(fields)
    print(f"\nEncoded message (hex): {encoded.hex()}")
    print(f"Encoded message (repr): {repr(encoded)}")
    print(f"Length: {len(encoded)} bytes")


def example_2_simple_decoding():
    """Example 2: Simple message decoding"""
    print("\n" + "="*60)
    print("Example 2: Simple Message Decoding")
    print("="*60)
    
    encoder = FIX42Encoder()
    decoder = FIX42Decoder()
    
    original = {
        '35': 'D',
        '49': 'TRADER',
        '56': 'BROKER',
        '55': 'AAPL',
        '54': '1',
        '38': '100',
    }
    
    # Encode
    encoded = encoder.encode(original)
    
    # Decode
    decoded = decoder.decode(encoded)
    
    print(f"\nOriginal fields: {original}")
    print(f"\nDecoded fields:")
    for tag in sorted(decoded.keys(), key=int):
        print(f"  Tag {tag}: {decoded[tag]}")


def example_3_roundtrip():
    """Example 3: Full roundtrip encode/decode"""
    print("\n" + "="*60)
    print("Example 3: Full Roundtrip")
    print("="*60)
    
    encoder = FIX42Encoder()
    decoder = FIX42Decoder()
    
    # New Order Single message
    order = {
        '35': 'D',
        '49': 'TRADER1',
        '56': 'BROKER',
        '34': '1',
        '52': '20240519-14:30:00',
        '55': 'MSFT',
        '54': '1',           # Buy
        '38': '500',
        '40': '2',           # Limit
        '44': '350.25',
    }
    
    print("\nOriginal Order:")
    print(f"  Symbol: {order['55']}")
    print(f"  Side: {'Buy' if order['54'] == '1' else 'Sell'}")
    print(f"  Quantity: {order['38']}")
    print(f"  Price: {order['44']}")
    
    # Encode to bytes
    encoded = encoder.encode(order)
    print(f"\nEncoded to {len(encoded)} bytes")
    
    # Verify checksum
    is_valid = decoder.verify_checksum(encoded)
    print(f"Checksum valid: {is_valid}")
    
    # Decode back
    decoded = decoder.decode(encoded)
    
    print("\nDecoded Order:")
    print(f"  Symbol: {decoded['55']}")
    print(f"  Side: {'Buy' if decoded['54'] == '1' else 'Sell'}")
    print(f"  Quantity: {decoded['38']}")
    print(f"  Price: {decoded['44']}")


def example_4_using_fixmessage_builder():
    """Example 4: Using FIXMessage builder"""
    print("\n" + "="*60)
    print("Example 4: FIXMessage Builder Pattern")
    print("="*60)
    
    # Build Logon message
    logon = FIXMessage('A')  # Logon
    logon.add_field('49', 'CLIENT')
    logon.add_field('56', 'SERVER')
    logon.add_field('34', '1')
    logon.add_field('98', '0')  # EncryptMethod: None
    logon.add_field('108', '30')  # HeartBtInt: 30 seconds
    
    print("\nLogon Message Fields:")
    for tag, value in logon.get_fields().items():
        print(f"  {tag}: {value}")
    
    # Encode
    encoder = FIX42Encoder()
    encoded = encoder.encode(logon.get_fields())
    
    print(f"\nEncoded to {len(encoded)} bytes")


def example_5_multiple_message_types():
    """Example 5: Multiple different message types"""
    print("\n" + "="*60)
    print("Example 5: Multiple Message Types")
    print("="*60)
    
    encoder = FIX42Encoder()
    decoder = FIX42Decoder()
    
    messages = [
        {
            'name': 'Logon',
            'fields': {
                '35': 'A',
                '49': 'CLIENT',
                '56': 'SERVER',
            }
        },
        {
            'name': 'NewOrderSingle (Buy Limit)',
            'fields': {
                '35': 'D',
                '49': 'TRADER',
                '56': 'BROKER',
                '55': 'AAPL',
                '54': '1',  # Buy
                '40': '2',  # Limit
                '44': '175.50',
            }
        },
        {
            'name': 'NewOrderSingle (Sell Market)',
            'fields': {
                '35': 'D',
                '49': 'TRADER',
                '56': 'BROKER',
                '55': 'GOOGL',
                '54': '2',  # Sell
                '40': '1',  # Market
            }
        },
        {
            'name': 'ExecutionReport',
            'fields': {
                '35': '8',
                '49': 'BROKER',
                '56': 'TRADER',
                '55': 'AAPL',
                '39': '2',  # OrdStatus: Filled
                '150': 'F',  # ExecType: Trade
            }
        },
    ]
    
    for msg in messages:
        encoder = FIX42Encoder()  # Reset
        encoded = encoder.encode(msg['fields'])
        decoded = decoder.decode(encoded)
        
        print(f"\n{msg['name']}:")
        print(f"  MsgType: {decoded['35']}")
        print(f"  Encoded size: {len(encoded)} bytes")
        print(f"  Checksum valid: {decoder.verify_checksum(encoded)}")


def example_6_error_handling():
    """Example 6: Error handling and validation"""
    print("\n" + "="*60)
    print("Example 6: Error Handling and Validation")
    print("="*60)
    
    encoder = FIX42Encoder()
    decoder = FIX42Decoder()
    
    # Valid message
    valid_msg = {
        '35': 'A',
        '49': 'CLIENT',
    }
    
    encoded_valid = encoder.encode(valid_msg)
    
    # Check valid checksum
    print(f"\nValid message checksum: {decoder.verify_checksum(encoded_valid)}")
    
    # Corrupt the checksum
    corrupted = encoded_valid.decode('utf-8').replace('10=', '10=ZZZ')
    print(f"Corrupted message checksum: {decoder.verify_checksum(corrupted)}")
    
    # Decode and handle missing fields
    decoded = decoder.decode(encoded_valid)
    symbol = decoded.get('55', 'N/A')
    print(f"Symbol (if present): {symbol}")


def example_7_field_access():
    """Example 7: Various ways to access decoded fields"""
    print("\n" + "="*60)
    print("Example 7: Field Access Methods")
    print("="*60)
    
    encoder = FIX42Encoder()
    decoder = FIX42Decoder()
    
    fields = {
        '35': 'D',
        '49': 'TRADER1',
        '55': 'IBM',
        '38': '1000',
    }
    
    encoded = encoder.encode(fields)
    
    # Method 1: Full dict
    decoded_dict = decoder.decode(encoded)
    print(f"\nMethod 1 - Full dict:")
    print(f"  decoded['35'] = {decoded_dict['35']}")
    
    # Method 2: get_field method
    print(f"\nMethod 2 - get_field method:")
    print(f"  decoder.get_field('35') = {decoder.get_field('35')}")
    print(f"  decoder.get_field('55') = {decoder.get_field('55')}")
    
    # Method 3: value method
    print(f"\nMethod 3 - value method:")
    value_dict = decoder.value()
    print(f"  decoder.value() = {value_dict['38']}")
    
    # Method 4: dict.get with default
    print(f"\nMethod 4 - dict.get with default:")
    print(f"  decoded['nonexistent'] with default = {decoded_dict.get('999', 'N/A')}")


if __name__ == '__main__':
    print("\n" + "#"*60)
    print("# FIX 4.2 Encoder/Decoder - Usage Examples")
    print("#"*60)
    
    example_1_simple_encoding()
    example_2_simple_decoding()
    example_3_roundtrip()
    example_4_using_fixmessage_builder()
    example_5_multiple_message_types()
    example_6_error_handling()
    example_7_field_access()
    
    print("\n" + "#"*60)
    print("# Examples completed successfully!")
    print("#"*60 + "\n")

