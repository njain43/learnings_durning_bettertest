"""A set is an unordered collection of elements without duplicate entries.
When printed, iterated or converted into a sequence, its elements will appear in an arbitrary order."""


def average(a: set) -> float:
    len_of_list = len(a)
    sum_of_list = sum(a)
    return sum_of_list / len_of_list


size_of_array = int(input())
ele_of_array = set(map(int, input().split()))

print(f'{average(ele_of_array):.3f}')
