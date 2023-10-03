from abc import ABC


class CustomException(Exception, ABC):
    """
    An abstract class to base other custom
    exceptions in the CodeLine module on.
    """


class BadOpcode(CustomException):
    """
    When raised, signifies that the current
    instruction isn't defined.
    """
    pass


class BadOperand(CustomException):
    """
    When raised, signifies that the current
    operands are invalid.
    """
    pass


class MemoryFull(CustomException):
    """
    When raised, signifies that the required
    memory has exceeded the available memory.
    """
    pass
