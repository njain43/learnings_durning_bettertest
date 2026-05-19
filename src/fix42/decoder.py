"""
FIX 4.2 Message Decoder - converts FIX protocol bytes to Python dict
"""

from src.fix42.message import SOH, format_fix_message_pipe_delimited


class FIX42Decoder:
    """Decodes FIX 4.2 messages from binary format to dictionary"""
    
    def __init__(self):
        self._decoded_fields = {}
    
    def decode(self, message: bytes) -> dict:
        """
        Decodes a FIX 4.2 message from bytes to dictionary.
        
        Args:
            message: bytes containing FIX encoded message
            
        Returns:
            dict: Dictionary with tag as key and value as value
        """
        # Convert bytes to string using UTF-8
        if isinstance(message, bytes):
            message_str = message.decode('utf-8')
        else:
            message_str = message
        
        # Replace SOH with separator for splitting
        message_str = message_str.replace(SOH, '|')
        
        # Split by separator and parse
        fields = message_str.split('|')
        
        self._decoded_fields = {}
        
        for field in fields:
            if '=' in field:
                tag, value = field.split('=', 1)
                self._decoded_fields[tag] = value
        
        return self._decoded_fields
    
    def verify_checksum(self, message: bytes) -> bool:
        """
        Verify the checksum of a FIX message.
        
        Args:
            message: bytes containing FIX encoded message
            
        Returns:
            bool: True if checksum is valid
        """
        if isinstance(message, bytes):
            message_str = message.decode('utf-8')
        else:
            message_str = message
        
        # Find the checksum field
        if SOH not in message_str:
            return False
        
        # Split to get checksum part
        parts = message_str.rsplit(SOH, 2)  # Split from right to get last SOH
        
        if len(parts) < 2:
            return False
        
        message_without_checksum = parts[0] + SOH
        checksum_part = parts[1]
        
        # Extract checksum value
        if '=' in checksum_part:
            tag, checksum_value = checksum_part.split('=')
            if tag != '10':
                return False
            
            # Calculate expected checksum
            expected_checksum = self._calculate_checksum(message_without_checksum.encode('utf-8'))
            
            return str(checksum_value.strip()) == expected_checksum
        
        return False
    
    def _calculate_checksum(self, data: bytes) -> str:
        """Calculate FIX checksum (sum of all bytes mod 256)"""
        checksum = sum(data) % 256
        return f'{checksum:03d}'
    
    def get_field(self, tag: str) -> str:
        """Get a specific field value by tag"""
        return self._decoded_fields.get(tag, '')
    
    def get_decoded_fields(self) -> dict:
        """Return all decoded fields"""
        return self._decoded_fields.copy()
    
    def value(self) -> dict:
        """Return decoded fields (compatible with existing codec pattern)"""
        return self._decoded_fields.copy()
    
    def get_formatted_message(self) -> str:
        """
        Get the decoded message as pipe-delimited string for easy reading.
        
        Returns:
            str: Message in format "8=FIX.4.2|9=123|35=D|..."
            
        Example:
            >>> decoder.decode(encoded_bytes)
            >>> print(decoder.get_formatted_message())
            8=FIX.4.2|9=123|35=D|49=SENDER|56=TARGET|10=192|
        """
        return format_fix_message_pipe_delimited(self._decoded_fields)
    
    def print_formatted_message(self, prefix: str = "") -> None:
        """
        Print the decoded message in pipe-delimited format.
        
        Args:
            prefix: Optional prefix to print before the message
            
        Example:
            >>> decoder.decode(encoded_bytes)
            >>> decoder.print_formatted_message("Decoded: ")
        """
        formatted = self.get_formatted_message()
        if prefix:
            print(prefix + formatted)
        else:
            print(formatted)

