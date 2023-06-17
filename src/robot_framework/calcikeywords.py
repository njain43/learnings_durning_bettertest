from robot.api.deco import keyword, library
from abc import ABC
from src.random_program.calculator import Calculator


@library(scope='GLOBAL', version='0.0.1', auto_keywords=False)
class CalculatorKeyworkds(ABC):


    @keyword
    def adding_two_numbers(self, a: int, b: int) -> int:
        self.calci = Calculator(a, b)
        return self.calci.add()

    @keyword
    def substract_two_numners(self, a: int, b: int) -> int:
        self.calci = Calculator(a, b)
        return self.calci.substract()
