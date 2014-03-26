
import types

from bento.core_exceptions import *
from bento.typed_list import _TypedList


class _OrderedProperty(object):
    
    counter = 0

    @classmethod
    def get_counter_and_increment(cls):
        cls.counter += 1
        return cls.counter


class _BaseProperty(object):

    _allowed_args = ['doc', 'validator', 'content_type']

    def __init__(self, default=None, required=False, *args, **kwargs):

 
        self._property_index = _OrderedProperty.get_counter_and_increment()

        if required not in (True, False):
            raise MiscError("'required' argument must be True or False.")
        else:
            self.required_property = required
        
        if args:
            raise KeylessArgError()

        self._content_type = kwargs.pop('content_type', object)

        self._keys = {}
        for key,value in kwargs.items():
            if key in self._allowed_args:
                self._keys[key] = value
            else:
                raise NotAllowedArgument("Not Allowed Key: %s" % key)
        
        self._key_meta_validation()

        if default is not None:
            self._type_validation(default)
            self._implicit_validation(default)
            self.__validate(default)
            self._default_value = default

    def _type_validation(self, value):
        # validation level 0

        if isinstance(value, self._content_type) or issubclass(self._content_type, type(value)):
            # If one of those two is true, the validation schema is okay
            return

        # else, something is not okay
        raise TypeError("%s got '%s' argument, expected '%s'" % (self.__class__.__name__, type(value).__name__, self._content_type.__name__))


    def _key_meta_validation(self):
        # validation level 1-a
        """
            This method checks if the key arguments are valid as keys
            For instance, if checks if key max isn't less or equal than key min
        """

    def _implicit_validation(self, value):
        # validation level 1-b
        """
            The implicit validation uses general keys to valid the property
            Examples of keys are: max, min, etc.
            Available keys may change from one property to another, check the 
            API reference for valid keys for each property
        """

    def __validate(self, value):
        # validation level 2
        """
            The validate function is a wrapper to the externally provided
            validation function
        """
        if 'validator' in self._keys:
            if not self._keys['validator'](value):
                raise TypeError("Validation function for '%s' does not accept value '%s'" % (self, value))


    def __get__(self, instance, cls):
        
        if not hasattr(self, 'attr_name'):
            attr_name = self._get_attr_name(instance)
            self.attr_name = '_attributename_' + attr_name
        else:
            attr_name = self.attr_name[len('_attributename_'):]

        if hasattr(instance, '_lazy_pointers') and attr_name in instance._lazy_pointers:
            if attr_name in instance._cached_properties:
                return instance._cached_properties[attr_name]
            function = instance._lazy_pointers[attr_name]
            value = function()
            self._type_validation(value)
            self._implicit_validation(value)
            self.__validate(value)
            instance._cached_properties[attr_name] = value
            return value
        elif hasattr(instance, self.attr_name):
            return getattr(instance, self.attr_name)
        elif hasattr(self, '_default_value'):
            return self._default_value

        # if all fails, return None

    def __set__(self, instance, value):
        self._type_validation(value)
        self._implicit_validation(value)
        self.__validate(value)

        if not hasattr(self, 'attr_name'):
            self.attr_name = '_attributename_' + self._get_attr_name(instance)

        #after changing any property, cache must be cleaned
        self._clean_cache(instance) #TODO -> this must be a 'instance' method
        setattr(instance, self.attr_name, value)

    def _get_attr_name(self, instance):
        if not hasattr(self, 'attr_name'):
            for attr_name, attr_value in instance.__class__.__dict__.items():
                if attr_value == self:
                    return attr_name

    def _clean_cache(self, instance):
        try:
            if not instance._strongly_cached_properties:
                instance._cached_properties = {}
            else:
                to_remove = [key for key in instance._cached_properties if key not in instance._strongly_cached_properties]
                for key in to_remove:
                    del(instance._cached_properties[key])
        except AttributeError:
            instance._cached_properties = {}


class StringProperty(_BaseProperty):

    def __init__(self, *args, **kwargs):
        super(StringProperty, self).__init__(*args, content_type=str, **kwargs)


class NumberProperty(_BaseProperty):

    _allowed_args = _BaseProperty._allowed_args + ['min', 'max']

    def __init__(self, *args, **kwargs):
        super(NumberProperty, self).__init__(*args, content_type=float, **kwargs)

    def _type_validation(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("%s got '%s' argument, expected '%s' or '%s'" % (self.__class__.__name__, type(value).__name__, int.__name__, float.__name__))


    def _implicit_validation(self, value):
    
        if 'max' in self._keys and value > self._keys['max']:
            raise InvalidArgument("Argument %s is grater than maximum allowed value %f." % (value, self._keys['max']))

        if 'min' in self._keys and value < self._keys['min']:
            raise InvalidArgument("Argument %s is lower than minimum allowed value %f." % (value, self._keys['min']))

    def _key_meta_validation(self):

        if 'max' in self._keys and hasattr(self, '_key_min'):
            if self._keys['max'] <= self._keys['min']:
                raise InvalidKeyValueError("Key 'max' must be greater than key 'min'.")


class PositiveNumberProperty(NumberProperty):
    
    def _implicit_validation(self, value):

        super(PositiveNumberProperty, self)._implicit_validation(value)

        if value <= 0:
            raise InvalidArgument("Argument %f must be a positive value")

    def _key_meta_validation(self):

        if 'min' in self._keys and self._keys['min'] < 0:
            raise InvalidKeyValueError("Key 'min' must be a positive value.")
        
        if 'max' in self._keys and self._keys['max'] < 0:
            raise InvalidKeyValueError("Key 'max' must be a positive value.")
        
        super(PositiveNumberProperty, self)._key_meta_validation()


class NonNegativeNumberProperty(PositiveNumberProperty):
    
    def _implicit_validation(self, value):

        super(PositiveNumberProperty, self)._implicit_validation(value)

        if value < 0:
            raise InvalidArgument("Argument %f must be a positive value")


class IntegerProperty(NumberProperty):

    def _implicit_validation(self, value):
        
        if not isinstance(value, int):
            raise InvalidArgument("Argument %s value is not an integer number.")

        super(IntegerProperty, self)._implicit_validation(value)


class PositiveIntegerProperty(IntegerProperty):

    def _implicit_validation(self, value):

        super(PositiveIntegerProperty,self)._implicit_validation(value)

        if value < 0:
            raise InvalidArgument("Argument %i is not an positive integer" % value)

    def _key_meta_validation(self):

        if 'min' in self._keys and self._keys['min'] < 0:
            raise InvalidKeyValueError("Key 'min' must be a positive value.")
        
        if 'max' in self._keys and self._keys['max'] < 0:
            raise InvalidKeyValueError("Key 'max' must be a positive value.")
        
        super(PositiveIntegerProperty, self)._key_meta_validation()


class BooleanProperty(_BaseProperty):
    
    def _implicit_validation(self, value):

        if not isinstance(value, bool):
            raise InvalidArgument("Argument %s type is not Boolean.")


class ObjectProperty(_BaseProperty):

    def __init__(self, *args, **kwargs):
        
        from bento.objects import Bento    #FIXME: inside-objects imports are not a good idea!

        if not 'content_type' in kwargs:
            kwargs['content_type'] = Bento
        
        super(ObjectProperty, self).__init__(*args, **kwargs)

    def __set__(self, instance, value):
        
        super(ObjectProperty, self).__set__(instance, value)

        self._object_definition = type(value)

    def _implicit_validation(self, value):
        
        from bento.objects import Bento    #FIXME: inside-objects imports are not a good idea!
        
        if not isinstance(value, Bento):
            raise InvalidArgument("Argument %s is not an valid %s instance." % (value, Bento))


class ListProperty(_BaseProperty):

    _allowed_args = _BaseProperty._allowed_args + ['list_content_type',]

    def __init__(self, *args, **kwargs):
        list_content_type = kwargs.pop('content_type', object)
        #kwargs['default'] = _TypedList(content_type=list_content_type)
        kwargs['content_type'] = _TypedList
        kwargs['list_content_type'] = list_content_type

        super(ListProperty,self).__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not isinstance(value, (tuple, list)):
            raise InvalidArgument("Argument '%s' must be a sequence, not %s" % (value,type(value)))

        if 'content_type' in self._keys:
            value = _TypedList(value, content_type=self._content_type)
        super(ListProperty, self).__set__(instance, value)

    def __get__(self, instance, cls):
        value = super(ListProperty, self).__get__(instance, cls)
        if value is None:
            self.__set__(instance, _TypedList(content_type=self._keys['list_content_type']))
            return super(ListProperty, self).__get__(instance, cls)
        else:
            return value
            
    def _implicit_validation(self, value):

        if not isinstance(value, list):
            raise InvalidArgument()
        if value:
            for obj in value:
                if not isinstance(obj, self._keys['list_content_type']):
                    raise InvalidArgument('Argument "%s" is not of type "%s"' % (obj, self._keys['list_content_type']))
#            if not all(map(lambda obj : isinstance(obj, self._keys['list_content_type']), value)):
#                raise InvalidArgument()


class LockedProperty(_BaseProperty):
    def __set__(self, instance, value):
        super(LockedProperty,self)._BaseProperty(instance, value)


class FunctionProperty(_BaseProperty):
    def __init__(self, *args, **kwargs):
        super(FunctionProperty, self).__init__(*args, content_type=types.FunctionType, **kwargs)


def ObjectListProperty(**kwargs):
    from bento.objects import Bento
    return ListProperty(content_type=Bento, *kwargs)


def DefinedObjectListProperty(content_type, **kwargs):
    from bento.objects import Bento
    if issubclass(content_type, Bento):
        return ListProperty(content_type=content_type, *kwargs)
    else:
        raise InvalidArgument("%s is not an Bento object" % content_type)


class TupleProperty(_BaseProperty):
    def __init__(self, *args, **kwargs):
        super(TupleProperty, self).__init__(*args, content_type=tuple, **kwargs)


class Tuple2Property(TupleProperty):
    def _implicit_validation(self, value):
        if len(value) != 2:
            raise BaseException("Tuple2Property must contains exactly 2 elements") 
        a,b = value
        if not isinstance(a,(int,float)) or not isinstance(b,(int,float)):
            raise BaseException("Tuple content must be float or integer")



