
"""
    This class is a workaround to create a base class in Python 3 style.
    This will trow a syntax error when running on a Python 2 environment
"""


def get_p27_metaclass(_IobjMetaclass):

    cdef class _Iobj:
        __metaclass__ = _IobjMetaclass
        pass

    return _Iobj
