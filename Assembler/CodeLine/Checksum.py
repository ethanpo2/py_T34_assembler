from .Memory import Memory


class Checksum(Memory):
    def __init__(self, line, addr, prev: list, num):
        """
        Stores the raw string, line number, address, optional label, and list
        of previous Lines. Throws a BadOperand exception if the line length is
        greater than 64.

        :param line: The raw string
        :param addr: The memory address
        :param prev: The list of previous Lines
        :param num: The line number
        """
        super().__init__(line, addr, num)
        self.__prev: list = prev

    def chk(self):
        """
        :return: The XOR checksum of the previous lines
        """
        chk = 0
        for p in self.__prev:
            chk ^= p.chk()
        return chk

    def __len__(self):
        return 1

    def __str__(self):
        opc = self.assembly()
        return "{:<15}{:>2} {}".format(opc, self.num(), self.raw())

    def assembly(self):
        hex_chk = hex(self.chk()).upper()
        return "{0}: {1:2}".format(
            hex(self.addr()).removeprefix("0x").upper(),
            hex_chk[len(hex_chk) - 2:]
        )
