import json

from src.converter_indexer import samples
from pathlib import Path


class Indexer:

    def __init__(self, fields_data: str = None, msg_data: str = None):

        # default fileds and msg files
        self._fields_file = (
                    Path(samples.__file__).parent / 'fields.json').read_text() if fields_data is None else fields_data
        self._order_file = (Path(
            samples.__file__).parent / 'order.json').read_text() if msg_data is None else msg_data

        self._fields = json.loads(self._fields_file)
        self._msg = json.loads(self._order_file)

    def __str__(self):
        print(self.fn2ft2fd())

    def fn2ft2fd(self) -> dict:
        fn2ft2fd = {}
        for value in self._fields['message_definition']:
            f_name = value['name']
            f_type = value['type']
            f_value = self._msg[f_name]
            fn2ft2fd.update({f_name: {"f_name": f_name, 'f_type': f_type, 'f_value': f_value}})

        return fn2ft2fd
