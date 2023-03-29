from unittest import TestCase
from src.codec.encoder import ByteEncoder


class TestEncoder(TestCase):

    def setUp(self):
        self._x = ByteEncoder()

    def test_int(self):
        self._x.uint_16(8)
        self.assertEqual(b'\x08\x00', self._x.value())

    def test_char_array(self):
        self._x.char_arr('NewOrderSingle')
        self.assertEqual(b'NewOrderSingle', self._x.value())
