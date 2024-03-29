# Lambda functions in Python are like little helpers that you can ask to do something for you.
# They are like small pieces of code that you can create and then use whenever you need them.

# For example, let's say you want to add two numbers together.
# Normally, you would write a function that takes two numbers as inputs and then returns the sum.
# But with a lambda function, you can write a short piece of code that does the same thing, like this:


# lambda arguments: expression
# e.g add = lambda x,y : x + y

add = lambda x, y, z: x + y + z
print(add(5, 6, 7))

double = lambda x: x * x
print(double(3))

print(list(map(double, [1, 2, 3, 4])))
print(list(map(lambda x: x * x * x, [1, 2, 3, 4])))

# filter out even numbers
print(f'Filter out even numbers {(list(filter(lambda x: x % 2 != 0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])))}')

from functools import reduce

print(f'Factorial - {(reduce(lambda x, y: x * y, [1, 2, 3, 4, 5]))}')
