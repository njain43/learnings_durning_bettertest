"""
A list has price of a security for 10 differet days, starting from day1 to day 10.
Find out the 2 days for buy/sell to generate max profit.

"""


class MinMax:

    def __init__(self, l: list):
        self.price_list = l

    def get_max_value_from_list(self):
        return max(self.price_list)

    def get_min_value_from_list(self):
        return min(self.price_list)

    def get_profit(self):
        return self.get_max_value_from_list() - self.get_min_value_from_list()


class MaxPossibleProfit:

    def __init__(self, list_of_price):
        self.list_of_price = list_of_price

    def get_indx(self, price: int | float = None) -> int:
        if price is None:
            price = self.list_of_price[0]
        return self.list_of_price.index(price)

    def check_sell_possibility(self, price_indx : int):
        pass

    def get_profit(self) -> int | float:
        indx_buy_price = self.get_indx()
        indx_sell_price = None
        buy_price = self.list_of_price[0]
        sell_price = self.list_of_price[0]
        for i in self.list_of_price:
            if i < buy_price and (indx_sell_price is None or self.get_indx(i) > indx_sell_price):
                buy_price = i
                indx_buy_price = self.get_indx(buy_price)
            elif i > sell_price and self.get_indx(i) > indx_buy_price:
                sell_price = i
                indx_sell_price = self.get_indx(sell_price)

        return sell_price - buy_price
