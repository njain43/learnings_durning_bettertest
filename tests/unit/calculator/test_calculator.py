from src.calculator import Calculator
from unittest import TestCase


class TestCalculator(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print(f'this is only called once at the begning of test cases')
        cls.calci = Calculator(4, 3)

    def setUp(self) -> None:
        print(f'this is  called  at begning of each test cases')
        # self.calci = Calculator(3, 4)

    @classmethod
    def tearDownClass(cls) -> None:
        print(f'this is only called at the end of test suite')

    def tearDown(self) -> None:
        print(f'this is called at the end of each testcase')

    def test_addition(self):
        self.assertEqual(7, self.calci.add())

    def test_substraction(self):
        self.assertEqual(1, self.calci.substract())

    def test_multiplication(self):
        self.assertEqual(12,self.calci.multiply())
