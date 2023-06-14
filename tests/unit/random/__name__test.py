from unittest import TestCase
from src.random import understading__name__ as mod

class RandomTestCase(TestCase):

    def test___name__(self):
        res = mod.hello_world()
        print(help(mod))
        self.assertEqual(f'hello src.random.understading__name__', res)
