import datetime
import unittest
import time

from src.random_program.default_mutable_argument import DateTimeInDifferentFormat


class TestDefaultMutableArgument(unittest.TestCase):

    def test_time_with_default_arugment(self):
        t1 = DateTimeInDifferentFormat.incorrect_way_of_timestamp()
        time.sleep(5)
        t2 = DateTimeInDifferentFormat.incorrect_way_of_timestamp()
        self.assertEqual(t1, t2)
        print(
            f' It shows that even after sleep of 5 secs, t1 {t1} and t2-{t2} are same because default argument in the '
            f'function fix_timestamp() get only executed once, and it retains the value.')

        print(f'The default argument value is evaluated only once at the time of function definition,'
              f' and subsequent calls to the function will retain and share the same mutable object.')

    def test_time_without_using_default_argument(self):
        t1 = DateTimeInDifferentFormat.incorrect_way_of_timestamp(datetime.datetime.now())
        time.sleep(2)
        t2 = DateTimeInDifferentFormat.incorrect_way_of_timestamp(datetime.datetime.now())
        print(f'different values of t1{t1} and t2-{t2}')
        self.assertNotEqual(t1, t2)

    def test_correct_way(self):
        t1 = DateTimeInDifferentFormat.correct_way()
        time.sleep(2)
        t2 = DateTimeInDifferentFormat.correct_way()
        print(f'different values of t1{t1} and t2-{t2}')
        self.assertNotEqual(t1, t2)



