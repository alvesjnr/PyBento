# Welcome to Bento - Properties for Python 3

Bento is a library that implements defined types properties for Python 3.

## Example

The best way to show how Bento properties works is by a simple example:

```
#!python

from core.objects import Bento
from core.properties import NumberProperty, StringProperty


class User(Bento):
    name = StringProperty()
    phone = NumberProperty()

 
user_1 = User(name="Mario", phone=887766)
user_2 = User("Luigi", phone=1234) # properties can be initializated by position

try:
    # type checking
    user_3 = User(name=9080, phone=123)
except TypeError:
    user_3 = User("Peach", 8888)

dumped = user_3.dump() # dump the content to a dictionary
print(dumped)
# {'name': 'Peach', 'phone': 8888}

# Create a new instance from the dumped dictionary
user_4 = User.load(dumped)

print(user_4.name, user_4.phone)
# Peach 8888

```


