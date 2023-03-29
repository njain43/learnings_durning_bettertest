from unittest import TestCase

from src.converter_indexer.converter import Converter


class TestIndexer(TestCase):

    def setUp(self) -> None:
        self._conv = Converter()
        # print(self._conv)

    def test_1(self):
        self.assertEqual(b'NewOrderSingle\x15\x00INFYfffff\x84\x94@NiteshBIOCNSE', self._conv.json2bytes())
