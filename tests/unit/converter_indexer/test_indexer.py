from unittest import TestCase
from src.converter_indexer.indexer import indexer


class TestIndexer(TestCase):

    def setUp(self) -> None:
        self._indx = indexer().fn2ft2fd()

    def test_indexer(self):
        self.assertEqual('NewOrderSingle', self._indx['MsgType'].get('f_value'))
        self.assertEqual(21, self._indx['Quantity'].get('f_value'))
