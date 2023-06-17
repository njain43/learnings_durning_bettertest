# list
lst = [1, 2, 3, 4, 5, 'hello', True]

# set: sets are useful in case of i) removing duplicates from list, ii) doing operations like union, intersection etc.
sset = {1, 2, 3, 4, 5, True, "Hello"}

# dict
dct = {'a': 1, 'b': 2}

print(type(lst), type(sset), type(dct))
print(lst, sset, dct)

set1 = {1, 3, 4, 5}
set2 = {2, 3, 6, 7}
print(f'intersection of set1 and set 2 - {(set1.intersection(set2))}')
print(f'union of set1 and set 2 - {(set1.union(set2))}')
print(f'difference of set1 and set 2 - {(set1.difference(set2))}')
