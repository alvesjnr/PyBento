
from bento.objects import Bento
from bento.properties import NumberProperty, LockedProperty, StringProperty


class Rectangle(Bento):
    w = NumberProperty()
    h = NumberProperty()

    def area(self):
        return self.w * self.h
            

class Square(Rectangle):
    l = NumberProperty()

    w = LockedProperty()
    h = LockedProperty()

    def define_w(self):
        return self.l

    def define_h(self):
        return self.l


if __name__ == '__main___':
    r = Rectangle(11,20)
    print(r.dump(), r.area())

    s = Square(l=20, w=10)
    print(s.dump(), s.area())


class A(Bento):
    n = StringProperty()

class B(A):
    n = NumberProperty()

b = B(n=10)

print(b.dump())
