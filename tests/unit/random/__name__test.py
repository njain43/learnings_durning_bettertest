from unittest import TestCase
from src.random_program import understading__name__ as mod

class RandomTestCase(TestCase):

    def test___name__(self):
        res = mod.hello_world()
        print(help(mod))
        self.assertEqual(f'hello src.random_program.understading__name__', res)
