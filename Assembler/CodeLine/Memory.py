from abc import ABC, abstractmethod
from .Line import Line


class Memory(Line, ABC):
    """
    A type of Line that is included in the object file.
    Serves as an abstract class for Opcode and Checksum.
    """
    def __init__(self, line: str, addr: int, num):
        """
        Stores the raw string, line number, address, and optional label.
        Throws a BadOperand exception if the line length is greater
        than 64.

        :param line: The raw string
        :param addr: The memory address
        :param num: The line number
        """
        super().__init__(line, num)
        self.__symbol = line[0:9].strip()
        self.__addr = addr

    @abstractmethod
    def __len__(self):
        """
        :return: The number of bytes in the assembly. Defaults to 0.
        """
        pass

    @abstractmethod
    def chk(self):
        pass

    def addr(self):
        """
        :return: The memory address
        """
        return self.__addr

    def symbol(self):
        """
        :return: The optional label
        """
        return self.__symbol

    @abstractmethod
    def assembly(self):
        """
        :return: The generated assembly in a ready-to-write format.
        """
        pass
