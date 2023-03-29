from src.codec.encoder import ByteEncoder

from src.converter_indexer.indexer import Indexer


class Converter:

    def __init__(self):
        self._indx = Indexer().fn2ft2fd()

    def json2bytes(self):
        def get_packet_value(d_type: str, val):
            b = ByteEncoder()

            # TODO convert below to matchcase after upgrading to 3.10
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

        return b''.join(bt_arr)


    # def bytes2json(self):
    #     def get_unpacked_values(f_type, val):
    #         b = Byte()
    #
    #         # TODO convert below to matchcase after upgrading to 3.10
    #         if "uint_16" == d_type:
    #             b.uint_16(val)
    #             return b.value()
    #         if "uint_8" == d_type:
    #             b.unit_8(val)
    #             return b.value()
    #         if "char_arr" == d_type:
    #             b.char_arr(val)
    #             return b.value()
    #         if "char" == d_type:
    #             b.char(val)
    #             return b.value()
    #         if "float" == d_type:
    #             b.float(val)
    #             return b.value()
