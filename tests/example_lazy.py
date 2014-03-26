"""
    This code shows the difference between a define_something and 
        a lazy_define_something
"""

from bento.objects import Bento
from bento.properties import IntegerProperty


# Now is up to you decide when you need to use lazy_define_something

class A(Bento):

    value = IntegerProperty(default=3)

    def define_value(self):
        return 3

a1 = A()
class B(A):

    def lazy_define_value(self):
        return 1

a2 = A()
b1 = B()
a3 = A()

n = 3 
print(a1.value, '==', n, a1.value == n)
print(a2.value, '==', n, a2.value == n)
n = 1
print(b1.value, '==', n, b1.value == n)
n = 3
print(a3.value, '==', n, a3.value == n)


