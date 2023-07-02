"""
Writing a file with `with`, a context manager.
With automatically closes the resources once it exits the loop.
"""

with open('test_file', 'w') as file:
    file.write('Writing in test file via python program\n')


with open('set_list.py', 'r') as f_read:
    print(f_read.read(7))  # -> read 7 chars


with open('set_list.py', 'r') as f_read:
    print(f' readline - {f_read.readline()}')  # -> read first line


with open('set_list.py', 'r') as f_read:
    print(f' readline - {f_read.readlines()}')  # -> read complete file


# Now without the context manager.

f = open('test_file', 'w')
f.write('hello world without context manager, dont forget to close the file')
f.close()