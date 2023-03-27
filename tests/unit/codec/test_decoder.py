from unittest import TestCase
from src.codec.decoder import ByteDecoder


class TestEncoder(TestCase):

    def setUp(self):
        self._x = ByteDecoder()

    def test_int(self):
        self._x.uint_16(b'\x08\x00')
        self.assertEqual(8, self._x.value())
