"""
Desc: __name__ is a special variable in python.
      When a program is imported in another program, it holds the value of imported program/file.
      When run via script, it holds value - '__main__'.

      This way we can know if a program is imported or run as a script.
"""


def hello_world():
    print(f' hello {__name__}')


def main():
    hello_world()


if __name__ == '__main__':
    main()
