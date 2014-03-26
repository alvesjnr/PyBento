
import unittest
from bento.properties import _BaseProperty
from bento.properties import *
from bento.properties import Tuple2Property, NumberProperty, LockedProperty
from bento.objects import Bento


class TestBaseProperty(unittest.TestCase):

    def test_a_base_property_basic_consistence(self):
        A = self.get_class_a()
        a = A()
        a.a = 10
        self.assertTrue(isinstance(a.__class__.__dict__['a'], _BaseProperty))

    def test_b_default_value(self):
        B = self.get_class_with_default()
        b = B()
        self.assertTrue(b.b == 10)

    def test_c1_validator(self):
        pass

    def test_d_doc(self):
        D = self.get_class_with_doc()
        d = D()
        #self.assertTrue(d.d.doc == "Yes, this is doc!") #FIXME!!!
    
    @staticmethod
    def get_class_a():
        class A(object):
            a = _BaseProperty()

        return A

    @staticmethod
    def get_class_with_default():
        class B(object):
            b = _BaseProperty(default=10)

        return B

    @staticmethod
    def get_class_with_validator(validator):
            class C(object):
                c = _BaseProperty(validator=validator)

            return C

    @staticmethod
    def get_class_with_doc():
        class D(object):
            d = _BaseProperty(doc="Yes, this is doc!")

        return D


class TestIntegerProperty(unittest.TestCase):

    @staticmethod
    def get_class():
        class A(Bento):
            value = IntegerProperty()

        return A

    def test_a_integer_property(self):
        a = self.get_class()(10)
        self.assertTrue(a.value == 10)

    def test_b_dump(self):
        a = self.get_class()(10)
        self.assertTrue(a.dump() == {'value': 10})

    def test_b_load(self):
        A = self.get_class()
        a = A.load({'value':88})
        self.assertTrue(a.value == 88)



class TestListProperty(unittest.TestCase):

    @staticmethod
    def get_class_a():
        class A(Bento):
            values = ListProperty()

        return A()

    @staticmethod
    def get_class_b():
        class B(Bento):
            values = ListProperty(content_type=str)

        return B()

    def test_a_default_value(self):
        a = self.get_class_a()
        self.assertTrue(a.values == [])

    def test_b_add_things_to_list(self):
        a = self.get_class_a()
        for i in range(10):
            a.values.append(i)
        self.assertTrue(a.values == [i for i in range(10)])

    def test_c_add_correct_type_value(self):
        b = self.get_class_b()
        for i in range(10):
            b.values.append(str(i))
        self.assertTrue(b.values == [str(i) for i in range(10)])

    def test_d_add_incorrect_type_value(self):
        b = self.get_class_b()
        self.assertRaises(InvalidArgument,b.values.append,10)

    def test_e_check_list_type(self):
        class E(Bento):
            l = ListProperty(content_type=str)

        self.assertTrue(E(l=['1']).dump() == {'l':['1']})
        self.assertRaises(InvalidArgument,E,['1',2])
        self.assertRaises(InvalidArgument, E, 12)
        self.assertRaises(InvalidArgument, E, [12])
    
    def test_f_multiple_instances_with_list(self):

        class O(Bento):
            v = IntegerProperty()

        class E(Bento):
            l = DefinedObjectListProperty(content_type=O)

        e1 = E(l=[O(v=1), O(v=2)])
        e2 = E()
        e2.l.append(O(v=3))
        
        self.assertTrue(e1.dump() == {'l': [{'v': 1}, {'v': 2}]})
        self.assertTrue(e2.dump() == {'l': [{'v': 3}]})

    def test_g_multiple_instances_with_list(self):

        class O(Bento):
            v = IntegerProperty()

        class E(Bento):
            l = DefinedObjectListProperty(content_type=O)

        e1 = E()
        e1.l.append(O(1))
        e1.l.append(O(2))

        e2 = E()
        e2.l.append(O(v=3))

        self.assertTrue(e1.dump() == {'l': [{'v': 1}, {'v': 2}]})
        self.assertTrue(e2.dump() == {'l': [{'v': 3}]})


class TestLockedProperty(unittest.TestCase):

    def setUp(self):

        class Circle(Bento):
            radius = NumberProperty(required=True)
            center = Tuple2Property()

        self.Circle = Circle


    @unittest.skip(reason="not yet implemented")
    def test_lockingProperty(self):

        class B(self.Circle):
            center = LockedProperty()
            def define_center(self):
                return (0.0, 0.0)

        self.assertTrue(False) # not testing nothing:wq!



if __name__ == '__main__':
    unittest.main()
