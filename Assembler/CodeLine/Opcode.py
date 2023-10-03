from .Memory import Memory
from .Op_Param import op_params
from .Exceptions import *


# noinspection PyBroadException
class Opcode(Memory):
    """
    The standard Lines that get written to the object file.
    Should always have a memory address and an instruction.
    The exception is Checksum because it behaves differently.
    """
    TABLE = {
        'ADC': {
            'imm': '69',
            'zrp': '65',
            'zpx': '75',
            'abs': '6D',
            'abx': '7D',
            'aby': '79',
            'inx': '61',
            'iny': '71'
        },
        'AND': {
            'imm': '29',
            'zrp': '25',
            'zpx': '35',
            'abs': '2D',
            'abx': '3D',
            'aby': '39',
            'inx': '21',
            'iny': '31'
        },
        'ASL': {
            'acc': '0A',
            'zrp': '06',
            'zpx': '16',
            'abs': '0E',
            'abx': '1E'
        },
        'BCC': {'rel': '90'},
        'BCS': {'rel': 'B0'},
        'BEQ': {'rel': 'F0'},
        'BIT': {
            'zrp': '24',
            'abs': '2C'
        },
        'BMI': {'rel': '30'},
        'BNE': {'rel': 'D0'},
        'BPL': {'rel': '10'},
        'BRK': {'imp': '00'},
        'BVC': {'rel': '50'},
        'BVS': {'rel': '70'},
        'CLC': {'imp': '18'},
        'CLD': {'imp': 'D8'},
        'CLI': {'imp': '58'},
        'CLV': {'imp': 'B8'},
        'CMP': {
            'imm': 'C9',
            'zrp': 'C5',
            'zpx': 'D5',
            'abs': 'CD',
            'abx': 'DD',
            'aby': 'D9',
            'inx': 'C1',
            'iny': 'D1'
        },
        'CPX': {
            'imm': 'E0',
            'zrp': 'E4',
            'abs': 'EC'
        },
        'CPY': {
            'imm': 'C0',
            'zrp': 'C4',
            'abs': 'CC'
        },
        'DEC': {
            'zrp': 'C6',
            'zpx': 'D6',
            'abs': 'CE',
            'abx': 'DE'
        },
        'DEX': {'imp': 'CA'},
        'DEY': {'imp': '88'},
        'EOR': {
            'imm': '49',
            'zrp': '45',
            'zpx': '55',
            'abs': '4D',
            'abx': '5D',
            'aby': '59',
            'inx': '41',
            'iny': '51'
        },
        'INC': {
            'zrp': 'E6',
            'zpx': 'F6',
            'abs': 'EE',
            'abx': 'FE'
        },
        'INX': {'imp': 'E8'},
        'INY': {'imp': 'C8'},
        'JMP': {
            'abs': '4C',
            'ind': '6C'
        },
        'JSR': {'abs': '20'},
        'LDA': {
            'imm': 'A9',
            'zrp': 'A5',
            'zpx': 'B5',
            'abs': 'AD',
            'abx': 'BD',
            'aby': 'B9',
            'inx': 'A1',
            'iny': 'B1'
        },
        'LDX': {
            'imm': 'A2',
            'zrp': 'A6',
            'zpx': 'B6',
            'abs': 'AE',
            'aby': 'BE',
        },
        'LDY': {
            'imm': 'A0',
            'zrp': 'A4',
            'zpx': 'B4',
            'abs': 'AC',
            'abx': 'BC',
        },
        'LSR': {
            'acc': '4A',
            'zrp': '46',
            'zpx': '56',
            'abs': '4E',
            'abx': '5E',
        },
        'NOP': {'imp': 'EA'},
        'ORA': {
            'imm': '09',
            'zrp': '05',
            'zpx': '15',
            'abs': '0D',
            'abx': '1D',
            'aby': '19',
            'inx': '01',
            'iny': '11'
        },
        'PHA': {'imp': '48'},
        'PHP': {'imp': '08'},
        'PLA': {'imp': '68', },
        'PLP': {'imp': '28'},
        'ROL': {
            'acc': '2A',
            'zrp': '26',
            'zpx': '36',
            'abs': '2E',
            'abx': '3E',
        },
        'ROR': {
            'acc': '6A',
            'zrp': '66',
            'zpx': '76',
            'abs': '6E',
            'abx': '7E',
        },
        'RTI': {'imp': '40'},
        'RTS': {'imp': '60', },
        'SBC': {
            'imm': 'E9',
            'zrp': 'E5',
            'zpx': 'F5',
            'abs': 'ED',
            'abx': 'FD',
            'aby': 'F9',
            'inx': 'E1',
            'iny': 'F1'
        },
        'SEC': {'imp': '38'},
        'SED': {'imp': 'F8'},
        'SEI': {'imp': '78'},
        'STA': {
            'zrp': '85',
            'zpx': '95',
            'abs': '8D',
            'abx': '9D',
            'aby': '99',
            'inx': '81',
            'iny': '91'
        },
        'STX': {
            'zrp': '86',
            'zpy': '96',
            'abs': '8E'
        },
        'STY': {
            'zrp': '84',
            'zpx': '94',
            'abs': '8C'
        },
        'TAX': {'imp': 'AA'},
        'TAY': {'imp': 'A8'},
        'TSX': {'imp': 'BA'},
        'TXA': {'imp': '8A'},
        'TXS': {'imp': '9A'},
        'TYA': {'imp': '98'}
    }

    def __init__(self, line: str, addr, symbols: dict, num):
        """
        First, stores the raw string, line number, address, optional label,
        instruction, and parameters. Then, replaces any symbol it can with the
        corresponding value. Finally, marks any symbols that need to replaced
        later. Throws a BadOperand exception if the line length is greater
        than 64.

        :param line: The raw string
        :param addr: The memory address
        :param symbols: The latest symbol table
        :param num: The line number
        """
        super().__init__(line, addr, num)

        self.__instr = line[9:14].strip()
        self.__params = line[14:25].strip()
        self.__missing = False

        temp = sorted(symbols.items(), key=lambda symbol: len(symbol[0]), reverse = True)
        for k, v in temp:
            if k in self.__params:
                val = int(v, 16)
                if 'rel' in self.__get_modes():
                    val = self.__abs_to_rel(val)

                hex_val = hex(val).replace('0x', '$').upper()
                self.__params = self.__params.replace(k, hex_val)

        try:
            params = self.params_to_op()
            if params:
                int(params, 16)
        except (ValueError, BadOperand):
            self.__missing = True

    def params_to_op(self):
        """
        :return: The parameters as a hex string
        """
        return op_params(self.params())

    def instr(self):
        """
        :return: The instruction
        """
        return self.__instr

    def params(self):
        """
        :return: The parameters
        """
        return self.__params

    def __get_modes(self):
        """
        Retrieves the addressing modes associated with the
        instruction. If the instruction isn't in the opcode table, a
        BadOpcode error is raised.

        :return: The addressing modes associated with the instruction.
        """
        try:
            return Opcode.TABLE.get(self.instr()).keys()
        except AttributeError:
            print(f"Bad opcode in line: {self.num()}")
            raise BadOpcode()

    def byte_params(self):
        """
        Converts the parameters into byte code. If there is a
        Bad Branch error, then dummy bytes are returned.

        If the instruction isn't in the opcode table, a BadOpcode
        error is raised. If the parameters can't be converted to
        hex, a BadOperand error is raised.

        :return: The parameters in byte code form
        """
        i = 0
        byte_params = []
        if self.__missing:
            if 'rel' in self.__get_modes():
                return ['1', '']
            else:
                return ['1', '2']

        try:
            params = self.params_to_op()
        except ValueError as e:
            print(f"Bad operand in line: {self.num()}")
            raise BadOperand(e)
        if len(params) % 2 == 1:
            params = f"0{params}"
        while i < 2 and params:
            byte_params.append(params[len(params) - 2:])
            params = params[:len(params) - 2]
            i += 1

        while len(byte_params) < 2:
            byte_params.append('')
        return byte_params

    def __abs_to_rel(self, val):
        """
        A helper function that converts the given absolute address
        to a relative address.

        :param val: An absolute address
        :return: val as a relative address
        """
        val -= self.addr() + 2
        if val < 0:
            val = 256 + val

        return val

    def replace_symbols(self, symbols: dict):
        """
        Finds and replaces any symbol that wasn't replaced in the first scan.

        :param symbols: The final symbol table
        """
        if not self.__missing:
            return
        else:
            self.__missing = False
        match = ('', '')
        for k, v in symbols.items():
            if k in self.params() and len(k) > len(match[0]):
                match = (k, v)

        if match[0]:
            val = int(match[1], 16)
            if 'rel' in self.__get_modes():
                val = self.__abs_to_rel(val)

            hex_val = hex(val).replace('0x', '$').upper()
            self.__params = self.__params.replace(match[0], hex_val)

    def mode(self):
        """
        Determines the mode of the instruction based on what modes are in the
        instruction's opcode table.

        :return:
        """
        modes = self.__get_modes()
        byte_params = self.byte_params()

        if 'imp' in modes and not self.params():
            return 'imp'
        elif 'acc' in modes and not self.params():
            return 'acc'
        elif 'imm' in modes and self.params().startswith('#'):
            return 'imm'
        elif self.params().startswith('('):
            if 'iny' in modes and self.params().endswith("),Y"):
                return 'iny'
            if 'inx' in modes and self.params().endswith(",X)"):
                return 'inx'
            if 'ind' in modes:
                return 'ind'
        elif self.params().endswith(',X'):
            if 'zpx' in modes and (self.__missing or not byte_params[1]):
                return 'zpx'
            if 'abx' in modes and byte_params[1]:
                return 'abx'
        elif self.params().endswith(',Y'):
            if 'zpy' in modes and (self.__missing or not byte_params[1]):
                return 'zpy'
            if 'aby' in modes and byte_params[1]:
                return 'aby'
        elif 'rel' in modes and (self.__missing or not byte_params[1]):
            return 'rel'
        elif 'zrp' in modes and (self.__missing or not byte_params[1]):
            return 'zrp'
        elif 'abs' in modes and byte_params[1]:
            return 'abs'

        return None

    def __len__(self):
        i = 1
        if self.error():
            return 0
        for b in self.byte_params():
            if b:
                i += 1

        return i

    def assembly(self):
        return "{0}: {1:2} {2[0]:2} {2[1]:2}".format(
            hex(self.addr()).removeprefix("0x").upper(),
            self.opcode(),
            self.byte_params()
        )

    def __str__(self):
        """
        Formats the Line's assembly and raw string into a console ready
        format. Also checks for Bad branch, Bad address mode, and BadOperand
        errors.

        :return: The Line's info in a console ready format.
        """
        error = self.error()
        if error == 'bbr':
            opc = ''
            return "Bad branch in line: {0}\n{1:<15}{0:>2} {2}".format(
                self.num(), opc, self.raw()
            )

        if error == 'bam':
            opc = ''
            return "Bad address mode in line: {0}\n{1:<15}{0:>2} {2}".format(
                self.num(), opc, self.raw()
            )

        opc = self.assembly()
        return "{:<15}{:>2} {}".format(opc, self.num(), self.raw())

    def chk(self):
        """
        :return: The XOR checksum of the Line's bytes
        """
        error = self.error()
        if error:
            return 0
        chk = int(self.opcode(), 16)

        for p in self.byte_params():
            if p != '':
                chk ^= int(p, 16)
        return chk

    def opcode(self):
        """
        :return: The Line's opcode
        """
        mode = self.mode()
        if 'rel' in self.__get_modes() and self.byte_params()[1]:
            mode = 'rel'
        return Opcode.TABLE.get(self.instr(), {}).get(mode, '')

    def error(self):
        byte_params = self.byte_params()
        if 'rel' in self.__get_modes() and byte_params[1]:
            return 'bbr'
        if self.opcode() == '':
            return 'bam'
        try:
            if self.params():
                int(byte_params[0], 16)
        except ValueError:
            print(f'Bad operand in line: {self.num()}')
            raise BadOperand()

        return ''
