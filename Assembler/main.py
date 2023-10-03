import sys

from CodeLine.Parser import Parser
from CodeLine.Exceptions import *


def main():
    """
    Reads in the source file contents and calls
    the CodeLine module.
    """
    try:
        try:
            in_file = open(sys.argv[1])
        except IndexError:
            print('syntax:\n\tpy main.py "filename"')
            return
        in_lines = in_file.readlines()
        in_file.close()
        out_lines = Parser(in_lines)
        out_lines.print()
        out_name = sys.argv[1].rsplit('.', 1)[0] + '.o'
        out_lines.write_to_file(out_name)

    except (BadOperand, MemoryFull, BadOpcode) as e:
        raise e


if __name__ == '__main__':
    main()
