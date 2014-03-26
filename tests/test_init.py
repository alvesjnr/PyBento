
import unittest
from bento.properties import *
from bento.objects import Bento


class _A(Bento):
    this_arg = StringProperty()
    other_arg = IntegerProperty(default=100)

class _B(_A):
    third_arg = StringProperty(required=True)



class TestInit(unittest.TestCase):
    
    def test_init_property_001(self):

        class A(_A):
            def init_this_arg(self):
                return "Ugent"

        a = A()
        self.assertTrue(a.this_arg == "Ugent")

    def test_init_property_002(self):

        class A(_A):
            def init_this_arg(self):
                return 99

        self.assertRaises(TypeError, A)

    def test_init_required_property_003(self):

        class B(_B):
            def init_third_arg(self):
                return "Intec"

        b = B()

        self.assertTrue(b.third_arg == "Intec")

    def test_init_required_property_004(self):
        class B(_B):
            def init_third_arg(self):
                return 99

        self.assertRaises(TypeError, B)


    def test_init_property_with_default_005(self):
        class A(_A):
            def init_other_arg(self):
                return 99

        a = A()
        self.assertTrue(a.other_arg == 99)


if __name__ == "__main__":
    unittest.main()

