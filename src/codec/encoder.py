from abc import ABC


class ByteEncoder(ABC):

    def __init__(self, value):
        self.value = value

    def unit_8(self, v: int) -> bytes:
        pass


