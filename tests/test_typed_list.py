
import unittest
from bento.typed_list import _TypedList, _AutomaticTypedList
from bento.core_exceptions import *


class TypedListTests(unittest.TestCase):

    ###################################
    # Part A - Testing Initialization #
    ###################################

    def test_001_list_of_integers(self):
        t = _TypedList([1,2,3,4])
        self.assertTrue(t == [1,2,3,4])

    def test_002_mixed_list(self):
        t = _TypedList([1,2,3,'4.4'])
        self.assertTrue(t == [1,2,3,'4.4'])

    def test_003_mixed_list(self):
        # same as: t = _TypedList([1,2,3,'4.4'], content_type=int)
        self.assertRaises(InvalidArgument, _TypedList, [1,2,3,'4.4'], content_type=int)

    def test_004_automatic_list(self):
        t = _AutomaticTypedList([1,2,3,4])
        self.assertTrue(t == [1,2,3,4])

    def test_010_empty_initialization(self):
        t = _TypedList()
        t = _TypedList(content_type=int)

    def test_011_automatic_list_empty_iitialization(self):
        # automatic list cannot by created without initial values
        self.assertRaises(TypeError, _AutomaticTypedList)
    
    def test_005_automatic_list_with_mixed_args(self):
        # same as: t = _AutomaticTypedList([1,2,3,'4.4'], content_type=float)
        self.assertRaises(TypeError, _AutomaticTypedList, [1,2,3,'4.4'], content_type=float)


    ##########################################
    # Part B - Testing insertion with append #
    ##########################################

    def test_006_appending_typed_list(self):
        t = _TypedList()
        t.append(1)
        t.append(3)
        self.assertTrue(t == [1, 3])
        t.append('8')
        self.assertTrue(t == [1, 3, '8'])

    def test_007_appending_typed_list(self):
        t = _TypedList(content_type=int)
        t.append(1)
        t.append(3)
        self.assertTrue(t == [1, 3])

        # same as: t.append('8')
        self.assertRaises(InvalidArgument, t.append, '8')

    def test_008_appending_typed_list(self):

        t = _TypedList([1, 2, 3], content_type=int)

        # same as: t.append('9.9')
        self.assertRaises(InvalidArgument, t.append, '9.9')

    def test_009_appending_automatic_list(self):
        t = _AutomaticTypedList([1,2,3])
        t.append(7)

        # same as: t.append('2')
        self.assertRaises(InvalidArgument, t.append, '2')

    def test_012_append_automatic_list(self):
        t = _AutomaticTypedList([1,2,3])
        t.append(7)
        self.assertTrue(t == [1, 2, 3, 7])

        # same as: t.append('9')
        self.assertRaises(InvalidArgument, t.append, '9')

        self.assertTrue(t == [1, 2, 3, 7])


    ###########################################
    # Part C - Testing insertion with __add__ #
    ###########################################

    def test_013_add_typed_list(self):
        t = _TypedList()
        t += [10, 11, 12]
        self.assertTrue(t == [10, 11, 12])
        self.assertTrue(t == _TypedList([10, 11, 12]))

    def test_014_add_typed_list(self):
        t = _TypedList([1])
        t += [10, 11, 12]
        self.assertTrue(t == [1, 10, 11, 12])
        self.assertTrue(t == _TypedList([1, 10, 11, 12]))

    def test_015_add_typed_list(self):
        t = _TypedList(content_type=str)
        t += ['19']
        self.assertTrue(t == ['19'])

        # same as: t += [5]
        self.assertRaises(InvalidArgument, t.__add__, [5,])

    def test_016_add_automatic_typed_list(self):
        t = _AutomaticTypedList([1,2])
        t += [99,]
        self.assertTrue(t == [1, 2, 99])

        # same as: t += ['bbt',]
        self.assertRaises(InvalidArgument, t.__add__, ['bbt', ])

        self.assertTrue(t == [1, 2, 99])


    ##########################################
    # Part E - Testing insertion with insert #
    ##########################################

    def test_017_insetion_typed_list(self):
        t = _TypedList([1, 2, 3, 4])
        t.insert(0, 99)
        t.insert(1, 'intec')

        self.assertTrue(t == [99, 'intec', 1, 2, 3, 4])

    def test_018_insertion_typed_list(self):
        t = _TypedList([1, 2, 3, 4], content_type=int)
        t.insert(0, 99)
        
        # same as: t.insert(1, 'intec')
        self.assertRaises(InvalidArgument, t.insert, 1, 'intec')
        self.assertTrue(t == [99, 1, 2, 3, 4])

    def test_019_insertion_automatic_list(self):
        t = _AutomaticTypedList([1, 2, 3, 4])
        t.insert(0, 99)
        
        # same as: t.insert(1, 'intec')
        self.assertRaises(InvalidArgument, t.insert, 1, 'intec')
        self.assertTrue(t == [99, 1, 2, 3, 4])

        
    ##########################################
    # Part D - Testing insertion with extend #
    ##########################################

    def test_020_extending_typed_list(self):
        t = _TypedList([1, 2, 3, 4])
        t.extend(['s', 1, 3])
        self.assertTrue(t == [1, 2, 3, 4, 's', 1, 3])
    
    def test_021_extending_typed_list(self):
        t = _TypedList([1, 2, 3, 4], content_type=int)
        
        # same as: t.extend([1, 's', 3])
        self.assertRaises(InvalidArgument, t.extend, [1, 's', 3])
        self.assertTrue(t == [1, 2, 3, 4])
    
    def test_022_extending_typed_list(self):
        t = _AutomaticTypedList("a b c d".split())
        
        # same as: t.extend(['s', 1, 3])
        self.assertRaises(InvalidArgument, t.extend, ['s', 1, 3])
        self.assertTrue(t == ['a', 'b', 'c', 'd'])

        t.extend("mnopq")
        self.assertTrue(t == ['a', 'b', 'c', 'd', 'm', 'n', 'o', 'p', 'q'])        
    

    ########################################
    # Part E - __setitem__ and __setlice__ #
    ########################################

    def test_023_setattr(self):
        t = _TypedList([1, 2, 3, 4], content_type=int)
        t[2] = 10
        self.assertTrue(t == [1, 2, 10, 4])

        # same as: t[3] = '8'
        self.assertRaises(InvalidArgument, t.__setitem__, 3, '8')
        self.assertTrue(t == [1, 2, 10, 4])

    def test_024_setslice(self):
        t = _TypedList([1, 2, 3, 4, 5, 6], content_type=int)
        t[1:3] = [10, 99, 77]
        self.assertTrue(t == [1, 10, 99, 77, 4, 5, 6])

        # same as: t[1:3] = [2, '8', 9.9]
        self.assertRaises(InvalidArgument, t.__setslice__, 1, 3, [2, '8', 9.9])
        self.assertTrue(t == [1, 10, 99, 77, 4, 5, 6])


if __name__=='__main__':
    unittest.main()
