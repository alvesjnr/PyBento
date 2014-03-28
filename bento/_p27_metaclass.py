
"""
    This class is a workaround to create a base class in Python 3 style.
    This will trow a syntax error when running on a Python 2 environment
"""

class _Iobj(object, metaclass=_IobjMetaclass):
     pass

def get_p27_metaclass(_IobjMetaclass):
    global _Iobj

    return _Iobj
