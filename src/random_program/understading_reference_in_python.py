location_dict = {
    'country': 'India',
    'cities': ['Indore', 'Pune', 'Mumbai']
}

a = location_dict

print(id(a) == id(location_dict))  # -> true

del a['cities']  # ->  This will delete from the mem location thus affecting both the dicts

print(location_dict)
print(id(a) == id(location_dict))


x = 10
y = a
print(id(x) == id(y))   #  False: Assignment does not create a reference to same object, rather creates a new object with same value.
print(id(x))
print(id(y))


"""
when we modify the dictionary through a, 
the change is also visible when accessing the dictionary through actual dict (location_dict). 
This is because a and location_dict are referencing the same dictionary object in memory.

It's important to note that this behavior applies to mutable objects like dictionaries, lists, and sets. 
For immutable objects like integers, strings, and tuples, assignment does not create a reference to the same object, 
but rather creates a new object with the same value.


Python handles memory management automatically using a mechanism called reference counting.
Whenever an object's reference count drops to zero, meaning no variables or references are pointing to it,
 Python's garbage collector deallocates the memory occupied by that object.
 
 It's worth noting that while Python handles memory deallocation for most objects, there are cases where you may need to explicitly release resources, such as closing files or database connections or network connections,to free up system resources. In such situations, it's important to follow best practices and use appropriate techniques, such as context managers (with statement) or explicit resource cleanup, to ensure proper resource deallocation
"""