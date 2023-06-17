

exchanges = ('NYSE', 'AQUIS', 'BATS', 'TRQ')
print(exchanges[3])
us_ex, atp, bats, mit = exchanges
print(us_ex, atp, bats, mit)

student = ('Nitesh', 'Jain', 'A')

# Now named tuples allows elements to be accessed by name instead of just by index.
from  collections import namedtuple

exchanges = namedtuple('Student', ['first', 'last', 'grade'])

