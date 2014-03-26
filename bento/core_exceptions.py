
class _BaseCoreException(BaseException):
    """
        Just a plcaeholder
    """

class MiscError(_BaseCoreException):
    """An error hapened!"""

class KeylessArgError(_BaseCoreException):
    """ Property accepts only key arguments """


class NotAllowedArgument(_BaseCoreException): 
    """ This value is not allowed to this property """

class InvalidKeyValueError(_BaseCoreException):
    """ The key is not valid """

class UnexpectedArgumentError(_BaseCoreException):
    """ Unexpected argument """

class ArgumentsArithmError(_BaseCoreException):
    """ Tobj got more arguments than expected """

class InvalidArgument(_BaseCoreException):
    """ Your argument is invalid """

class UnexpectedArgumentError(_BaseCoreException):
	""" Some argument was not expected """


class MaxLoadError(_BaseCoreException):
    pass

class MaxSizeError(_BaseCoreException):
    pass

class TimeAnomalyError(_BaseCoreException):
    pass

class UnknowMessageError(_BaseCoreException):
    pass

class DuplicatedParameterError(_BaseCoreException):
    pass
