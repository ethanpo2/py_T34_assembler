from operator import itemgetter

from .Opcode import Opcode
from .Checksum import Checksum
from .NOpcode import NOpcode
from .Memory import Memory
from .Op_Param import op_params
from .Exceptions import *


class Parser:
    """
    A container class for Lines. Generates and
    organizes Lines as well as the symbol table.
    Writes assembled code to the console and
    output file.
    """
    def __init__(self, str_lines: list):
        """
        Converts the source code into Lines. Also sorts said
        Lines into lists, so they can be operated on later without
        further sorting. After the symbol table has been calculated,
        goes back into the Lines and replaces any symbol with the
        corresponding value.

        :param str_lines: A list of lines taken from the source code.
        """
        self.__lines = []
        self.__memory = []
        self.__opcode = []
        self.__errors = []
        self.__symbols = {}
        self.__start = int('8000', 16)

        for line in str_lines:
            if 'ORG' in line[9:13]:
                num = line.split()[1]
                self.__start = int(num.removeprefix('$'), 16)

        curr = self.__start
        for i, line in enumerate(str_lines, 1):
            if len(line) > 64:
                raise ValueError()
            line = line.removesuffix('\n')
            line = f"{line:<63}\n"
            up_line = line.replace(line[:14], line[:14].upper())
            if up_line.startswith("*") or up_line.strip().startswith(';') or 'END' in up_line[9:13] or 'ORG' in up_line[9:13]:
                new_l = NOpcode(up_line, i)
                self.__lines.append(new_l)
            elif 'EQU' in up_line[9:13]:
                self.__store_equ(up_line, i, curr)
                new_l = NOpcode(up_line, i)
                self.__lines.append(new_l)
            elif 'CHK' in up_line[9:13]:
                new_l = Checksum(up_line, curr, self.__memory.copy(), i)
                self.__add_memory(new_l, i)
                curr += len(new_l)
            else:
                new_l = Opcode(up_line, curr, self.__symbols, i)
                self.__opcode.append(new_l)
                self.__add_memory(new_l, i)
                curr += len(new_l)

            if curr > int("FFFF", 16) or len(self.__symbols) > 255:
                print("Memory Full")
                raise MemoryFull()

        for line in self.__opcode:
            line.replace_symbols(self.__symbols)

    def __add_memory(self, line: Memory, num):
        """
        A helper function that operates on Memory objects (Memories)
        and serves several purposes.

        * Sorts Memories into their appropriate lists
        * Extracts symbols from Memories and adds them to the symbol table
        * Checks for duplicate symbols

        :param line: A newly created Memory
        :param num: The current line number
        """
        # noinspection PyTypeChecker
        self.__lines.append(line)
        self.__memory.append(line)
        if line.symbol():
            if line.symbol() not in self.__symbols.keys():
                self.__symbols[line.symbol()] = hex(line.addr()).removeprefix('0x').upper()
            else:
                error = f"Duplicate symbol in line: {num}"
                self.__errors.append(error)
                print(error)
                input('Press enter to continue...')

    def __store_equ(self, line: str, line_num: int, addr: int):
        """
        Parses a string containing the EQU instruction and stores
        their symbol in the symbol table. Also checks for duplicate
        symbols.

        :param line: An unparsed EQU string
        :param line_num: The current line number
        :param addr: The current memory address
        """
        symbol, _, val, *_ = line.split()
        if symbol not in self.__symbols.keys():
            val.replace("*", hex(addr).removeprefix('0x').upper())
            try:
                val = op_params(val)
            except ValueError as e:
                print(f"Bad operand in line: {line_num}")
                raise BadOperand(e)

            self.__symbols[symbol] = val
        else:
            error = f"Duplicate symbol in line: {line_num}"
            self.__errors.append(error)
            print(error)
            input('Press enter to continue...')

    def print(self):
        """
        Prints the parsed code and any non-fatal errors to the
        console.
        """
        print('Assembling')
        num_bytes = 0
        num_errors = len(self.__errors)
        for i, line in enumerate(self.__lines):
            try:
                print(str(line).format(i + 1), end="")
                if line.error() != '':
                    input('Press enter to continue...')
                num_bytes += len(line)
                if line.error() != '':
                    num_errors += 1
            except ValueError as e:
                print(f"Bad operand in line: {i + 1}")
                raise e

        print(f"\n--End assembly, {num_bytes} bytes, errors: {num_errors}\n")

        alpha = []
        num = []
        for k, v in self.__symbols.items():
            while len(v) < 2:
                v = f"0{v}"
            alpha.append((k, v))
            num.append((k, v))
        alpha.sort(key=itemgetter(0))
        num.sort(key=lambda tup: int(tup[1].removeprefix('$'), 16))

        def print_symbol(k, v):
            nonlocal curr_line, i
            curr_line += "{:<9}{:<9}".format(k, f"=${v}")
            i += 1
            if i % 4 == 0:
                print(curr_line)
                curr_line = '    '

        print(f"Symbol table - alphabetical order:")
        curr_line = '    '
        i = 0
        for k, v in alpha:
            print_symbol(k, v)

        print(curr_line)

        print(f"Symbol table - numerical order:")
        curr_line = '    '
        i = 0
        for k, v in num:
            print_symbol(k, v)

        print(curr_line, end="")

    def write_to_file(self, filename):
        """
        Writes the generated assembly to the given filename. The
        assembly consists of memory address and byte codes like so::

            MEM1: B1 B2 B3
            MEM2: B1 B2 B3
            MEM3: B1 B2 B3
            ...

        If the file already exists, its contents are overwritten.

        :param filename: Name of the file to write to
        """
        out_str = []
        if len(self.__errors):
            return
        for m in self.__memory:
            if m.error():
                return
            out_str.append(m.assembly() + '\n')
        out_str.append(out_str.pop().removesuffix('\n'))

        out = open(filename, 'w')
        out.writelines(out_str)
        out.close()
