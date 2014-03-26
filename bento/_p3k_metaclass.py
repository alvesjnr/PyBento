
"""
    This class is a workaround to create a base class in Python 3 style.
    This will trow a syntax error when running on a Python 2 environment
"""

def get_p3k_metaclass(_IobjMetaclass):
    class _Iobj(object, metaclass=_IobjMetaclass):
         pass

    return _Iobj
