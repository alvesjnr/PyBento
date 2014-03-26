
from bento.core_exceptions import *


class _TypedList(list):
    
    def __init__(self, values=None, content_type=object):

        if values is None:
            values = []

        self._content_type = content_type

        for value in values:
            self.__content_verification(value)
        
        super(_TypedList, self).__init__(values)
        
    def __content_verification(self, value):
        if hasattr(self, '_content_type') and self._content_type is not object:
            if not isinstance(value, self._content_type):
                raise InvalidArgument("Arguments '%s' does not follow type '%s'" % (value, self._content_type))
    
    def __add__(self, rvalue):
        
        if isinstance(rvalue, (list, tuple)):
            for i in rvalue:
                self.__content_verification(i)
        super(_TypedList, self).__add__(rvalue)

    def __setitem__(self, index, value):
        self.__content_verification(value)
        super(_TypedList, self).__setitem__(index, value)

    def __setslice__(self, i, j, iterable):
        for value in iterable:
            self.__content_verification(value)
        super(_TypedList, self).__setslice__(i, j, iterable)

    def append(self, value):
        self.__content_verification(value)
        super(_TypedList, self).append(value)

    def insert(self, index, value):
        self.__content_verification(value)
        super(_TypedList, self).insert(index,value)

    def extend(self, iterable):    
        for i in iterable:
            self.__content_verification(i)

        super(_TypedList, self).extend(iterable)


class _AutomaticTypedList(_TypedList):

    def __init__(self, values):
        
        content_type = type(values[0])
        super(_AutomaticTypedList, self).__init__(values=values, content_type=content_type)

