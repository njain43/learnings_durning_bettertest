from robot.api.deco import keyword, library
from abc import ABC
from src.random_program.calculator import Calculator


@library(scope='GLOBAL', version='0.0.1', auto_keywords=False)
class CalculatorKeywords(ABC):

    @keyword
    def adding_two_numbers(self, a: int, b: int) -> int:
        calci = Calculator(a, b)
        return calci.add()

    @keyword
    def subtract_two_numbers(self, a: int, b: int) -> int:
        calci = Calculator(a, b)
        return calci.substract()
