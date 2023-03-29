from src.codec.decoder import ByteDecoder
from src.codec.encoder import ByteEncoder
from src.converter_indexer.indexer import Indexer


class Converter:

    def __init__(self):
        self._indx = Indexer().fn2ft2fd()

    def json2bytes(self):
        def get_packet_value(d_type: str, val) -> list[bytes]:
            b = ByteEncoder()

            # TODO convert below to match case after upgrading to 3.10
            if "uint_16" == d_type:
                b.uint_16(val)
                return b.value()
            if "uint_8" == d_type:
                b.unit_8(val)
                return b.value()
            if "char_arr" == d_type:
                b.char_arr(val)
                return b.value()
            if "char" == d_type:
                b.char(val)
                return b.value()
            if "float" == d_type:
                b.float(val)
                return b.value()

        bt_arr = []
        for k, v in self._indx.items():
            f_type = v['f_type']
            f_val = v['f_value']
            bt_arr.append(get_packet_value(f_type, f_val))

        # return b''.join(bt_arr)
        return bt_arr

    def bytes2json(self, buffer: bytes) -> dict:
        def get_unpacked_values(d_type, val):
            b = ByteDecoder()

            # TODO convert below to match case after upgrading to 3.10
            if "uint_16" == d_type:
                b.uint_16(val)
                return b.value()
            if "uint_8" == d_type:
                b.unit_8(val)
                return b.value()
            if "char_arr" == d_type:
                b.char_arr(val)
                return b.value()
            if "char" == d_type:
                b.char(val)
                return b.value()
            if "float" == d_type:
                b.float(val)
                return b.value()

        final_json = {}
        indx = 0
        for k, v in self._indx.items():
            f_type = v['f_type']
            f_name = v['f_name']
            val = get_unpacked_values(f_type, buffer[indx])
            final_json[f_name] = val
            indx += 1

        return final_json
