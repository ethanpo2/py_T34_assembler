from abc import ABC

from .Exceptions import *


class Line(ABC):
    """
    An abstract class to serve as a base for other Line classes.
    """
    def __init__(self, line: str, num: int):
        """
        Stores the raw string and line number.
        Throws a BadOperand exception if the line length is greater
        than 64.

        :param line: The raw string
        :param num: The line number
        """
        if len(line) > 64:
            raise BadOperand()
        self.__raw = line.rstrip() + '\n'
        self.__num = num

    def __len__(self):
        """
        Returns the number of bytes in the assembly. Defaults to 0.

        :return: The number of bytes
        """
        return 0

    def error(self):
        """
        Determines if there are any errors in the Line. The possible errors are:

        * **Non-Fatal**
        * Bad branch (bbr) - a branch instruction point to an out-of-range address
        * Bad address mode (bam) - the instruction exists but not with the given mode
        * **Fatal**
        * Bad operand - the operand cannot be converted to an integer

        :return: An error abbreviation
        """
        return ''

    def raw(self):
        """
        :return: The raw string
        """
        return self.__raw

    def num(self):
        """
        :return: The line number
        """
        return self.__num

    def __str__(self):
        """
        :return: The Line's info a console ready format.
        """
        return "{:<15}{:>2} {}".format("", self.num(), self.raw())

