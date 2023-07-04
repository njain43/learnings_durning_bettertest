from datetime import datetime

"""
The default mutable argument value is evaluated only once at the time of function definition,'
              f' and subsequent calls to the function will retain and share the same mutable object

"""


class DateTimeInDifferentFormat:

    @staticmethod
    def incorrect_way_of_getting_timestamp(d: datetime = datetime.now()):
        return f'{d.strftime("%Y%m%d-%H:%M:%S")}'

    @staticmethod
    def correct_way(d: datetime = None):
        if d is None:
            d = datetime.now()
            return f'{d.strftime("%Y%m%d-%H:%M:%S")}'
        else:
            return f'{d.strftime("%Y%m%d-%H:%M:%S")}'

    # Immutable arguments will be used when no value is passed.
    @staticmethod
    def def_immutable_argument(d: datetime = f'20230702-19:33:56'):
        return d