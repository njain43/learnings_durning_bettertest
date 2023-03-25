class Calculator:

    def __init__(self, a: int = 1, b: int = 1):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b

    def substract(self):
        return self.a - self.b

    def multiply(self):
        return self.a * self.b

    def to_the_power(self):
        return self.a ** self.b


calci = Calculator(3, 4)
print(calci.add())
