from sinch.core.exceptions import SinchException


class NumbersException(SinchException):
    pass


class NumberNotFoundException(NumbersException):
    pass
