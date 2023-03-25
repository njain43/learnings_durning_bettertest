from unittest import TestCase
from src.converter_indexer.indexer import Indexer
from src.converter_indexer import samples
from pathlib import Path


class TestIndexer(TestCase):

    def setUp(self) -> None:
        self._indx = Indexer().fn2ft2fd()

    def test_indexer(self):
        self.assertEqual('NewOrderSingle', self._indx['MsgType'].get('f_value'))
        self.assertEqual(21, self._indx['Quantity'].get('f_value'))

    def test_indexer_with_another_msg(self):
        self._order_file = (Path(
            samples.__file__).parent / 'ExecutionReport.json').read_text()
        self._indx = Indexer(msg_data=self._order_file).fn2ft2fd()
        self.assertEqual('ExecutionReport', self._indx['MsgType'].get('f_value'))



