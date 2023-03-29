from unittest import TestCase
from pathlib import Path
from src.converter_indexer import samples
from src.converter_indexer.converter import Converter
import json

class TestIndexer(TestCase):

    def setUp(self) -> None:
        self._conv = Converter()

        self._order_file = (Path(
            samples.__file__).parent / 'order.json').read_text()

        self.expected_json = json.loads(self._order_file)


    def test_jsn2bytes(self):
        output = self._conv.json2bytes()
        # print(f'bytes- {output}')
        self.assertEqual([b'NewOrderSingle', b'\x15\x00', b'INFY', b'fffff\x84\x94@', b'Nitesh', b'B', b'IOC', b'NSE'], output)

    def test_bytes2json(self):
        jsn = self._conv.bytes2json(self._conv.json2bytes())
        # print(f'jsn - {jsn}')
        self.assertDictEqual(jsn, self.expected_json)
