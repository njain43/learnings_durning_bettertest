"""
FIX 4.2 Message Encoder - converts Python dict to FIX protocol bytes
"""

from src.fix42.message import SOH


class FIX42Encoder:
    """Encodes FIX 4.2 messages to binary format"""

    def __init__(self, begin_string: str = 'FIX.4.2'):
        self.begin_string = begin_string
        self._encoded_message = b''

    def encode(self, fields: dict) -> bytes:
        """
        Encodes a dictionary of fields into FIX 4.2 message format.

        Args:
            fields: Dictionary with tag as key (str) and value as value (str)

        Returns:
            bytes: FIX encoded message
        """
        # Prepare header
        header_fields = {}
        header_fields['8'] = self.begin_string

        # Calculate body length (all fields except BeginString, BodyLength, CheckSum)
        body_content = self._build_body_content(fields)
        body_length = len(body_content.encode('utf-8'))

        header_fields['9'] = str(body_length)

        # Build header
        header_part = self._build_header(header_fields)

        # Build body
        body_part = body_content

        # Build trailer with checksum
        message_without_checksum = header_part + body_part
        checksum = self._calculate_checksum(message_without_checksum.encode('utf-8'))

        # Final message
        self._encoded_message = (message_without_checksum + f'10={checksum}{SOH}').encode('utf-8')

        return self._encoded_message

    def _build_header(self, header_fields: dict) -> str:
        """Build the FIX header"""
        header = ''
        # Order: BeginString, BodyLength
        for tag in ['8', '9']:
            if tag in header_fields:
                header += f'{tag}={header_fields[tag]}{SOH}'
        return header

    def _build_body_content(self, fields: dict) -> str:
        """Build the message body content (fields between header and trailer)"""
        body = ''
        # Sort by tag for consistency (numerical sort)
        sorted_tags = sorted(fields.keys(), key=lambda x: int(x) if x.isdigit() else float('inf'))

        for tag in sorted_tags:
            value = fields[tag]
            body += f'{tag}={value}{SOH}'

        return body

    def _calculate_checksum(self, data: bytes) -> str:
        """Calculate FIX checksum (sum of all bytes mod 256)"""
        checksum = sum(data) % 256
        return f'{checksum:03d}'

    def get_encoded_message(self) -> bytes:
        """Return the last encoded message"""
        return self._encoded_message

    def value(self) -> bytes:
        """Return the last encoded message (compatible with existing codec pattern)"""
        return self._encoded_message

    def get_formatted_message(self) -> str:
        """
        Get the last encoded message as pipe-delimited string for easy reading.

        Returns:
            str: Message in format "8=FIX.4.2|9=123|35=D|..."
        """
        if not self._encoded_message:
            return ""

        # Decode the message and format it
        decoded_str = self._encoded_message.decode('utf-8')
        decoded_str = decoded_str.replace(SOH, '|')

        # Remove last SOH if present
        if decoded_str.endswith('|'):
            return decoded_str
        return decoded_str + '|'

    # def print_formatted_message(self, prefix: str = "") -> None:
    #     """
    #     Print the last encoded message in pipe-delimited format.
    #
    #     Args:
    #         prefix: Optional prefix to print before the message
    #
    #     Example:
    #         >>> encoder.encode({'35': 'A', '49': 'SENDER'})
    #         >>> encoder.print_formatted_message("Logon: ")
    #     """
    #     formatted = self.get_formatted_message()
    #     if prefix:
    #         print(prefix + formatted)
    #     else:
    #         print(formatted)
    #
