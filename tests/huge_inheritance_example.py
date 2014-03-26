from bento.objects import *
from bento.properties import *


class C(Bento):
    a = StringProperty(default='lsjkdfhlk')
    b = StringProperty(default='lsjkii934095830dfhlk')
    v = StringProperty(default='354576786')
    c = StringProperty(default='7868678')


class B(Bento):
    s = StringProperty()
    n = NumberProperty()
    o = ObjectListProperty()

    def define_o(self):
        k = []
        for i in range(100):
            k.append(C())
        return k


class A(Bento):
    a = ObjectListProperty()

    def define_a(self):
        k = []
        for i in range(10):
            k.append(B('243', 42345.88))
        return k


class Master(Bento):
    k = ObjectListProperty()

    def define_k(self):
        k = []
        for i in range(100):
            k.append(A())
        return k

m = Master()
m._touch()
