from unittest import TestCase
from src.random_program.max_difference_between_2_elements import MinMax, MaxPossibleProfit


class TestMinMax(TestCase):

    def setUp(self) -> None:
        sample_price_list = [1, 2, 4, 3, 8, 10, 9]
        share_price_list = [1, 4, .5, .3]
        self.obj = MinMax(sample_price_list)
        self.max_profit = MaxPossibleProfit(share_price_list)

    def test_get_max_value(self):
        self.assertEqual(10, self.obj.get_max_value_from_list())

    def test_get_min_value(self):
        self.assertEqual(1, self.obj.get_min_value_from_list())

    def test_profit(self):
        self.assertEqual(9, self.obj.get_profit())

    def test_max_profit(self):
        self.assertEqual(3.5, self.max_profit.get_profit())
