
import sys

from bento.properties import _BaseProperty, ObjectProperty, ListProperty, LockedProperty
from bento.core_exceptions import *


class _BentobjMetaclass(type):

    def __new__(cls, name, bases, dct):

        for base in bases:
            for key, value in base.__dict__.items():
                if isinstance(value,_BaseProperty):
                    dct[key] = base.__dict__[key]
                    # WARNING! potential bug!
                    # delattr(base, key)

        prop = {}
        for key,value in dct.items():
            if isinstance(value, _BaseProperty):
                prop[key] = (value.__class__, value._property_index)

        consecutive_arguments = [(key,value[1]) for key,value in prop.items()]
        consecutive_arguments.sort(key=lambda a : a[1])
        consecutive_arguments = [arg for arg,i in consecutive_arguments]

        dct.update({'_core_properties': prop,
                    '_consecutive_arguments': consecutive_arguments,
                    })
        
        return super(_BentobjMetaclass, cls).__new__(cls, name, bases, dct)





class _Bento(object):
    __metaclass__ = _BentobjMetaclass

    # def __init__(self, *args, **kwargs):
        
    #     self._cached_properties = {} #cache for define_ functions
    #     self._strongly_cached_properties = set() # define_functions which will never be removed from cache
    #     self._set_consecutive_arguments(args)

    #     for prop_name in self._consecutive_arguments[len(args):]:
    #         prop = self.__class__.__getattribute__(self.__class__,prop_name)
    #         if prop.required_property:
    #             if not prop_name in kwargs.keys():
    #                 if not hasattr(self, "init_%s" % prop_name) and not hasattr(self.__class__, "define_%s" % prop_name):
    #                     raise TypeError("Missing required value: '%s'" % prop_name)
        
    #     self.__explicity_values = []
    #     for key,value in kwargs.items():
    #         if key in self._core_properties:
    #             #TODO: locked
    #             # if isinstance(self.__class__.__getattribute__(self.__class__,key), LockedProperty):
    #             #     print(8888)
    #             self.__explicity_values.append(key)
    #             setattr(self, key, value)
    #         else:
    #             raise UnexpectedArgumentError("Got an unexpected key: '%s'" % key)
        
    #     self._lazy_pointers = {}
    #     self._define_properties()


    def _define_properties(self):
        """
            This function handle automatic definitions for properties

            class A(Bento):
                a = IntegerProperty()
                def init_a(self):
                    a = rand.random()
        """
        for prop in self._core_properties.keys():

            if prop in self.__explicity_values:
                continue

            init_name = "init_%s" % prop
            lazy = "define_%s" % prop
            if hasattr(self.__class__, lazy):
                f = getattr(self, lazy)
                self._lazy_pointers[prop] = f
                continue

            if hasattr(self, init_name):
                f = getattr(self, init_name)
                value = f()
                setattr(self, prop, value)
        

    def _set_consecutive_arguments(self, args):
        
        if len(args) > len(self._consecutive_arguments):
            raise ArgumentsArithmError()

        for arg,attr in zip(args, self._consecutive_arguments):
            setattr(self, attr, arg)

    def dump(self):
        """
            Convert it from object to structure
        """

        d = {}

        for arg in self._consecutive_arguments:
            if hasattr(self, arg):
                obj = getattr(self, arg)

                if isinstance(obj, Bento):
                    d[arg] = obj.dump()
                elif isinstance(obj,(list, tuple)):
                    if obj:
                        if isinstance(obj[0], Bento):
                            d[arg] = [v.dump() for v in obj]
                        else:
                            d[arg] = [v for v in obj]
                    else:
                        d[arg] = []
                else:
                    d[arg] = getattr(self, arg)

        return d

    @classmethod
    def load(cls, raw):
        """ 
            Recreate a Bento object based on a structure
        """
        bento_object = cls()

        for key,value in raw.items():

            if key in bento_object._core_properties:
                meta_obj = cls.__getattribute__(cls,key)
                
                if isinstance(meta_obj, ObjectProperty):
                    obj_class = meta_obj._object_definition
                    obj = obj_class.load(value)
                    setattr(bento_object, key, obj)

                elif isinstance(meta_obj, ListProperty):
                    obj_class = meta_obj._keys['list_content_type']
                    if issubclass(obj_class, Bento):
                        obj = [obj_class.load(v) for v in value]
                    else:
                        obj = [obj_class(v) for v in value]
                    setattr(bento_object, key, obj)

                else:
                    setattr(bento_object, key, value)
            
            else:
                raise UnexpectedArgumentError("%s got an unexpected argument named '%s'" % (cls, key))

        return bento_object

    def _touch(self):
        """
            Actually does nothing. Used for performance measurement
        """

        for arg in self._consecutive_arguments:
            if hasattr(self, arg):
                obj = getattr(self, arg)

                if isinstance(obj, Bento):
                    obj._touch()
                elif isinstance(obj,(list, tuple)):
                    if obj:
                        if isinstance(obj[0], Bento):
                            for v in obj:
                                v._touch()
                else:
                    getattr(self, arg)


class Bento(_Bento):

    def __init__(self, *args, **kwargs):
        
        self._cached_properties = {} #cache for define_ functions
        self._strongly_cached_properties = set() # define_functions which will never be removed from cache
        self._set_consecutive_arguments(args)

        for prop_name in self._consecutive_arguments[len(args):]:
            prop = self.__class__.__getattribute__(self.__class__,prop_name)
            if prop.required_property:
                if not prop_name in kwargs.keys():
                    if not hasattr(self, "init_%s" % prop_name) and not hasattr(self.__class__, "define_%s" % prop_name):
                        raise TypeError("Missing required value: '%s'" % prop_name)
        
        self.__explicity_values = []
        for key,value in kwargs.items():
            if key in self._core_properties:
                #TODO: locked
                # if isinstance(self.__class__.__getattribute__(self.__class__,key), LockedProperty):
                #     print(8888)
                self.__explicity_values.append(key)
                setattr(self, key, value)
            else:
                raise UnexpectedArgumentError("Got an unexpected key: '%s'" % key)
        
        self._lazy_pointers = {}
        self._define_properties()


def cache(function):
    """
        Cache decorator
    """

    def decorator(*args, **kwargs):
        self = args[0]
        prop_name = function.__name__[7:] # removing 'define_'
        self._strongly_cached_properties.add(prop_name)
        return function(*args, **kwargs)

    if function.__name__.startswith('define_'):
        return decorator
    else:
        return function
