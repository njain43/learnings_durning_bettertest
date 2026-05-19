"""
FIX 4.2 Message structure and utilities
"""

# FIX 4.2 Standard fields
FIX_HEADER_FIELDS = {
    '8': 'BeginString',      # FIX version (e.g., FIX.4.2)
    '9': 'BodyLength',       # Length of body
    '35': 'MsgType',         # Message type
}

FIX_TRAILER_FIELDS = {
    '93': 'SignLength',      # Signature length
    '89': 'Signature',       # Signature
    '10': 'CheckSum',        # Checksum
}

# Common field tags
FIX_COMMON_FIELDS = {
    '49': 'SenderCompID',
    '56': 'TargetCompID',
    '34': 'MsgSeqNum',
    '52': 'SendingTime',
    '55': 'Symbol',
    '54': 'Side',           # 1=Buy, 2=Sell
    '38': 'OrderQty',
    '40': 'OrdType',        # 1=Market, 2=Limit
    '44': 'Price',
}

# Message types
MESSAGE_TYPES = {
    'A': 'Logon',
    'D': 'NewOrderSingle',
    '8': 'ExecutionReport',
    '1': 'TestRequest',
}

SOH = '\x01'  # Start of Header - field separator


class FIXMessage:
    """Helper class for creating FIX messages"""
    
    def __init__(self, msg_type: str):
        self.msg_type = msg_type
        self.fields = {}
        self.fields['35'] = msg_type
    
    def add_field(self, tag: str, value: str):
        """Add a field to the message"""
        self.fields[tag] = str(value)
        return self
    
    def add_fields(self, fields_dict: dict):
        """Add multiple fields at once"""
        for tag, value in fields_dict.items():
            self.fields[tag] = str(value)
        return self
    
    def get_fields(self) -> dict:
        """Get all fields"""
        return self.fields.copy()


def format_fix_message_pipe_delimited(fields: dict, sort_by_tag: bool = True) -> str:
    """
    Format FIX message fields as pipe-delimited string.
    
    Args:
        fields: Dictionary with tag as key and value as value
        sort_by_tag: Whether to sort fields by tag number (default: True)
        
    Returns:
        str: Pipe-delimited message (e.g., "8=FIX.4.2|9=123|35=D|")
        
    Example:
        >>> fields = {'8': 'FIX.4.2', '9': '123', '35': 'D'}
        >>> format_fix_message_pipe_delimited(fields)
        '8=FIX.4.2|9=123|35=D|'
    """
    if sort_by_tag:
        # Sort by tag number
        sorted_tags = sorted(fields.keys(), key=lambda x: int(x) if x.isdigit() else float('inf'))
    else:
        sorted_tags = fields.keys()
    
    message_parts = []
    for tag in sorted_tags:
        message_parts.append(f'{tag}={fields[tag]}')
    
    return '|'.join(message_parts) + '|'


def print_fix_message_pipe_delimited(fields: dict, sort_by_tag: bool = True, prefix: str = "") -> None:
    """
    Print FIX message fields as pipe-delimited string.
    
    Args:
        fields: Dictionary with tag as key and value as value
        sort_by_tag: Whether to sort fields by tag number (default: True)
        prefix: Optional prefix to print before the message
        
    Example:
        >>> fields = {'8': 'FIX.4.2', '9': '123', '35': 'D', '49': 'TRADER'}
        >>> print_fix_message_pipe_delimited(fields)
        8=FIX.4.2|9=123|35=D|49=TRADER|
        
        >>> print_fix_message_pipe_delimited(fields, prefix="Message: ")
        Message: 8=FIX.4.2|9=123|35=D|49=TRADER|
    """
    formatted = format_fix_message_pipe_delimited(fields, sort_by_tag)
    if prefix:
        print(prefix + formatted)
    else:
        print(formatted)


