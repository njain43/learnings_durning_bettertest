"""
There is a list with numbers from 1 to 100 except for a missing numner
Find the missing number
"""

numbers = []
for i in range(1, 101):
    if i != 65:
        numbers.append(i)

sum_of_1_to_100 = 100 * (100 + 1) / 2  # n(n+1)/2
sum_of_given_numbers = sum(numbers)

missing_numbers = sum_of_1_to_100 - sum_of_given_numbers
print(f'missing number is - {missing_numbers}')


""
# Another way of finding missing number is using sets.

numbers_1_to_100_set = set()
for i in range(1, 101):
    numbers_1_to_100_set.add(i)

missing_numbers_1 = numbers_1_to_100_set.difference(numbers)
print(f'missing number is - {missing_numbers_1}')
print(f'missing number is - {",".join(map(str,missing_numbers_1))}')

