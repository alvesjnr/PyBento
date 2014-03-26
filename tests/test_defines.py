
import unittest
from bento.properties import *
from bento.objects import Bento, cache
import random


class _A(Bento):
    this_arg = StringProperty()
    other_arg = IntegerProperty(default=100)

class _B(_A):
    third_arg = StringProperty(required=True)



class TestDefine(unittest.TestCase):
    
    def test_define_property_001(self):

        class A(_A):
            def define_this_arg(self):
                return "Ugent"

        a = A()
        self.assertTrue(a.this_arg == "Ugent")

    def test_define_property_002(self):

        class A(_A):
            def define_this_arg(self):
                return 99
        a = A()
        self.assertRaises(TypeError, lambda : a.this_arg)

    def test_define_required_property_003(self):

        class B(_B):
            def define_third_arg(self):
                return "Intec"

        b = B()

        self.assertTrue(b.third_arg == "Intec")

    def test_define_required_property_004(self):

        self.assertTrue(TypeError, _B)

        class B(_B):
            def define_third_arg(self):
                return 'Light'
        
        self.assertTrue(B().third_arg == 'Light')


    def test_define_property_with_default_005(self):
        class A(_A):
            def define_other_arg(self):
                return 99

        a = A()
        self.assertTrue(a.other_arg == 99)


    def test_define_006(self):
        class A(_A):
            def define_this_arg(self):
                return "Gent"

        a = A()

        self.assertTrue(a.this_arg == "Gent")

    def test_define_required_property_007(self):

        class B(_B):
            def define_third_arg(self):
                return "Bruxelas"

        b = B()
        self.assertTrue(b.third_arg == "Bruxelas")

    def test_define_required_property_008(self):

        class B(_B):
            def define_third_arg(self):
                return 99

        b = B()
        self.assertRaises(TypeError, lambda : b.third_arg) #lambda is a work around to encapsulate the call



class TestAdvancedDefine(unittest.TestCase):

    def test_overwriting_define_009(self):

        class A(_A):
            def init_this_arg(self):
                return "Newton"

        a = A(this_arg="Leibniz")

        self.assertTrue(a.this_arg == "Leibniz")
    
    def test_overwriting_lazy_define_010(self):

        class A(_A):
            def define_this_arg(self):
                return "Newton"

        a = A(this_arg="Leibniz")

        self.assertTrue(a.this_arg == "Leibniz")


class TestCache(unittest.TestCase):


    def test_cache_init_001(self):
        # init_ isn't really cached, but acts like it 

        class A(Bento):
            a = NumberProperty()

            def init_a(self):
                return random.random()

        a = A()
        for i in range(100):
            self.assertTrue(a.a == a.a)

    def test_cache_define_002(self):

        class A(Bento):
            a = NumberProperty()

            def define_a(self):
                return random.random()

        a = A()
        for i in range(100):
            self.assertTrue(a.a == a.a)

    def test_cache_init_define_003(self):

        class A(Bento):
            a = NumberProperty()

            def define_a(self):
                return random.random()
            
            def init_a(self):
                return random.random()

        a = A()
        for i in range(100):
            self.assertTrue(a.a == a.a)

    def test_cache_define_004(self):
        """
            Test if, after setting a property, the cache is cleaned
        """

        class A(Bento):
            b = NumberProperty(required=True)
            a = NumberProperty()

            def define_a(self):
                return 2 * self.b
        
        a = A(b=5)
        self.assertTrue(a.a == 10)

        a.b = 6
        self.assertTrue(a.a == 12)


    def test_cache_define_005(self):

        class A(Bento):
            b = NumberProperty(required=True)
            a = NumberProperty()

            @cache
            def define_a(self):
                return random.random()
        
        a = A(b=5)

        for i in range(100):
            v1 = a.a
            a.b = 6
            v2 = a.a
            self.assertTrue(v1 == v2)



if __name__ == "__main__":
    unittest.main()

