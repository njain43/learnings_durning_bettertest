from unittest import TestCase
from src.codec.decoder import ByteDecoder


class TestDecoder(TestCase):

    def setUp(self):
        self._x = ByteDecoder()

    def test_int(self):
        self._x.uint_16(b'\x08\x00')
        self.assertEqual(8, self._x.value())

    def test_char_arr(self):
        self._x.char_arr(b'NewOrderSingle')
        self.assertEqual('NewOrderSingle', self._x.value())

    def test_char(self):
        self._x.char(b'N')
        self.assertEqual('N', self._x.value())

