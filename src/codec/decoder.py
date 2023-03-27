from abc import ABC
from struct import unpack


class ByteDecoder(ABC):

    def __init__(self):
        self._buf = b''

    def __str__(self):
        print(self._buf)

    def value(self):
        return self._buf[0]

    def unit_8(self, v: bytes):
        self._buf = ('<h', v)

    def uint_16(self, v: bytes):
        self._buf = unpack('<H', v)

    def string(self, v: bytes):
        self._buf = unpack('<s', v)

    def float(self, v: bytes):
        self._buf = unpack('d', v)

    def char(self, v: bytes):
        self._buf = unpack('<c', v.decode('utf-8'))
