from abc import ABC
from struct import pack


class ByteEncoder(ABC):

    def __init__(self):
        self._buf = b''

    def __str__(self):
        print(self._buf)

    def value(self):
        return self._buf

    def unit_8(self, v: int):
        self._buf = pack('<h', v)

    def uint_16(self, v: int):
        self._buf = pack('<H', v)

    def char_arr(self, v: str):
        self._buf = pack(str(len(v)) + "s", v.encode('utf-8'))


    def float(self, v: float):
        self._buf = pack('d', v)

    def char(self, v: str):
        self._buf = pack('<c', v.encode('utf-8'))
