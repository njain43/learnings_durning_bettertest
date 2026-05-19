# FIX 4.2 Encoder/Decoder Module

## Overview

This module provides a complete implementation of the FIX (Financial Information Exchange) 4.2 protocol encoder and decoder for Python. It enables serialization and deserialization of FIX messages used in financial trading systems.

## What is FIX Protocol?

FIX is a standard for financial messaging. FIX 4.2 uses:
- **SOH (0x01)** as the field separator (Start of Header)
- **Tag=Value** format for each field
- **Checksum** for message integrity
- Structured header and trailer

Example FIX message (with | representing SOH):
```
8=FIX.4.2|9=95|35=D|49=TRADER|56=BROKER|55=AAPL|54=1|38=100|40=2|44=150.50|10=234|
```

## Module Structure

```
src/fix42/
├── __init__.py          # Package initialization
├── encoder.py           # FIX42Encoder class
├── decoder.py           # FIX42Decoder class
└── message.py          # FIXMessage helper and constants
```

## Installation

No additional dependencies needed beyond what's in the project. Uses only Python's standard library.

## Quick Start

### Basic Encoding

```python
from src.fix42.encoder import FIX42Encoder

encoder = FIX42Encoder()

# Create a message
fields = {
    '35': 'D',           # MsgType: NewOrderSingle
    '49': 'TRADER1',     # SenderCompID
    '56': 'BROKER',      # TargetCompID
    '55': 'AAPL',        # Symbol
    '54': '1',           # Side: Buy
    '38': '100',         # OrderQty
    '40': '2',           # OrdType: Limit
    '44': '150.50',      # Price
}

# Encode to bytes
encoded = encoder.encode(fields)
print(encoded)
```

### Basic Decoding

```python
from src.fix42.decoder import FIX42Decoder

decoder = FIX42Decoder()

# Decode from bytes
decoded = decoder.decode(encoded)

print(decoded['35'])    # D
print(decoded['55'])    # AAPL
print(decoded['44'])    # 150.50
```

### Using FIXMessage Builder

```python
from src.fix42.message import FIXMessage

# Create a message using builder pattern
msg = FIXMessage('D')  # NewOrderSingle
msg.add_field('49', 'TRADER1')
msg.add_field('56', 'BROKER')
msg.add_field('55', 'MSFT')
msg.add_field('54', '2')  # Sell
msg.add_field('38', '500')

# Get fields and encode
fields = msg.get_fields()
encoder = FIX42Encoder()
encoded = encoder.encode(fields)
```

## Common FIX Message Types

| Code | Type | Usage |
|------|------|-------|
| A | Logon | Initial handshake between client and server |
| D | NewOrderSingle | Place a new order |
| 8 | ExecutionReport | Report on order execution |
| 1 | TestRequest | Heartbeat/connectivity test |

## Common FIX Field Tags

| Tag | Name | Example |
|-----|------|---------|
| 8 | BeginString | FIX.4.2 |
| 9 | BodyLength | 95 |
| 35 | MsgType | A, D, 8, 1 |
| 49 | SenderCompID | TRADER1 |
| 56 | TargetCompID | BROKER |
| 34 | MsgSeqNum | 1 |
| 52 | SendingTime | 20240519-10:30:00 |
| 55 | Symbol | AAPL |
| 54 | Side | 1=Buy, 2=Sell |
| 38 | OrderQty | 100 |
| 40 | OrdType | 1=Market, 2=Limit |
| 44 | Price | 150.50 |
| 10 | CheckSum | 234 |

## API Reference

### FIX42Encoder

```python
encoder = FIX42Encoder(begin_string='FIX.4.2')
```

**Methods:**
- `encode(fields: dict) -> bytes` - Encode fields to FIX message bytes
- `value() -> bytes` - Get the last encoded message
- `get_encoded_message() -> bytes` - Get the last encoded message

**Example:**
```python
encoder = FIX42Encoder()
msg_bytes = encoder.encode({'35': 'A', '49': 'CLIENT'})
```

### FIX42Decoder

```python
decoder = FIX42Decoder()
```

**Methods:**
- `decode(message: bytes|str) -> dict` - Decode FIX message to fields dictionary
- `verify_checksum(message: bytes|str) -> bool` - Verify message checksum
- `get_field(tag: str) -> str` - Get a specific field value
- `get_decoded_fields() -> dict` - Get all decoded fields
- `value() -> dict` - Get decoded fields

**Example:**
```python
decoder = FIX42Decoder()
fields = decoder.decode(msg_bytes)
if decoder.verify_checksum(msg_bytes):
    print("Message is valid")
```

### FIXMessage

```python
msg = FIXMessage(msg_type: str)
```

**Methods:**
- `add_field(tag: str, value: str) -> FIXMessage` - Add a single field (chainable)
- `add_fields(fields_dict: dict) -> FIXMessage` - Add multiple fields (chainable)
- `get_fields() -> dict` - Get all fields

**Example:**
```python
msg = FIXMessage('D')
msg.add_field('49', 'TRADER').add_field('55', 'AAPL')
fields = msg.get_fields()
```

## Real-World Examples

### Complete Order Flow

```python
from src.fix42.encoder import FIX42Encoder
from src.fix42.decoder import FIX42Decoder
from src.fix42.message import FIXMessage

# 1. Send Logon
logon = FIXMessage('A')
logon.add_fields({
    '49': 'CLIENT1',
    '56': 'BROKER',
    '34': '1',
    '52': '20240519-10:30:00',
})

encoder = FIX42Encoder()
logon_msg = encoder.encode(logon.get_fields())

# 2. Send NewOrderSingle
order = FIXMessage('D')
order.add_fields({
    '49': 'CLIENT1',
    '56': 'BROKER',
    '34': '2',
    '55': 'AAPL',
    '54': '1',  # Buy
    '38': '100',
    '40': '2',  # Limit
    '44': '150.50',
})

encoder = FIX42Encoder()
order_msg = encoder.encode(order.get_fields())

# 3. Receive ExecutionReport
exec_report_bytes = order_msg  # In real scenario, from server

decoder = FIX42Decoder()
execution = decoder.decode(exec_report_bytes)

if decoder.verify_checksum(exec_report_bytes):
    print(f"Order Symbol: {execution['55']}")
    print(f"Side: {execution['54']}")
    print(f"Quantity: {execution['38']}")
```

## Testing

Run all FIX 4.2 tests:

```bash
export PYTHONPATH=./src:./tests
python3 -m unittest discover -s tests/unit/fix42 -p "test_*.py" -v
```

**Test Coverage:**
- 28 unit tests for encoder/decoder functionality
- 10 integration tests for real-world scenarios
- Total: **38 tests** - all passing

## Implementation Details

### Message Structure

Every FIX message has:

1. **Header (3 fields minimum)**
   - BeginString (8) - FIX version
   - BodyLength (9) - Length of body
   - MsgType (35) - Message type

2. **Body**
   - All user-defined fields in tag=value format

3. **Trailer**
   - CheckSum (10) - Message checksum (sum of all bytes mod 256)

### Checksum Algorithm

```
checksum = sum(all_message_bytes) % 256
formatted_checksum = f'{checksum:03d}'
```

### Field Ordering

Fields are ordered numerically by tag number during encoding for consistency.

## Limitations & Notes

1. **FIX 4.2 Specifics** - This implementation targets FIX 4.2 standard
2. **No Repeating Groups** - FIX 4.2 has limited repeating group support
3. **String Values** - All field values are treated as strings
4. **UTF-8 Encoding** - Messages are encoded/decoded as UTF-8
5. **Little-Endian** - Follows FIX little-endian byte order for compatibility

## Common Use Cases

1. **Trading Systems** - Place and manage orders
2. **Execution Brokers** - Report executions to clients
3. **Market Data** - Distribute pricing and trade information
4. **Risk Management** - Monitor trading activity
5. **Compliance** - Audit and regulatory reporting

## Further Reading

- [FIX Protocol Official Specification](https://www.fixtrading.org/)
- [FIX 4.2 Specification PDF](https://www.fixtrading.org/standards/fix-4-2/)

## Contributing

When adding new features:
1. Add unit tests in `tests/unit/fix42/`
2. Ensure all existing tests pass
3. Update this documentation
4. Follow the existing code style and patterns

