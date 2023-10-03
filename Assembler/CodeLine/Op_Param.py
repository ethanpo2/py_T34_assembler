def to_dec(num: str):
    """
    Converts a string encoded number without any operands into an
    integer. Supports these formats:

    * HEX - $45
    * DEC - 65
    * OCT - o101 or O101
    * BIN - %01000101
    * ASC - 'A' or "A"

    Will raise a ValueError if there are spaces or the string
    doesn't match one of these formats.

    :param num: a number in string form
    :return: num converted to an integer
    """
    num = num.removeprefix('(').removeprefix('#').removesuffix(')')
    if num.startswith('$'):
        return int(num[1:], 16)
    if num.startswith(('O', 'o')):
        return int(num[1:], 8)
    if num.startswith('%'):
        return int(num[1:], 2)
    if num.startswith(("'", '"')):
        num = num.replace("'", "").replace('"', '')
        return ord(num)
    else:
        return int(num)


def op_params(expr: str):
    """
    Converts a string encoded math expression and converts it to a
    hexadecimal string. Supports the following operations:

    * \+ addition
    * \- subtraction
    * \* multiplication
    * / division
    * & bit-wise AND
    * . bit-wise OR
    * ! bit-wise XOR

    Will raise a ValueError if there are spaces in the string.

    :param expr: a mathematical expression in string form
    :return: the calculated expression as a hex string
    """
    op = []
    num = []
    expr = expr.split(',')[0]

    if not {'+', '-', '*', '/', '&', '!', '.'}.intersection(set(expr)):
        if expr:
            expr = to_dec(expr)
            return hex(expr).removeprefix('0x').upper()
        else:
            return ''

    def split_op(operation: str):
        nonlocal expr
        op.append(operation)
        p = expr.rsplit(operation, 1)
        num.append(p[1])
        expr = p[0]

    for letter in reversed(expr):
        if letter == ".":
            split_op(".")
        elif letter == '!':
            split_op('!')
        elif letter == '&':
            split_op('&')
        elif letter == '-':
            split_op('-')
        elif letter == '+':
            split_op('+')
        elif letter == '/':
            split_op('/')
        elif letter == '*':
            split_op('*')
    num.append(expr)

    for o in reversed(op):
        val1 = to_dec(num.pop())
        val2 = to_dec(num.pop())
        if o == '.':
            num.append(str(val1 | val2))
        elif o == '!':
            num.append(str(val1 ^ val2))
        elif o == '&':
            num.append(str(val1 & val2))
        elif o == '-':
            num.append(str(val1 - val2))
        elif o == '+':
            num.append(str(val1 + val2))
        elif o == '/':
            num.append(str(int(val1 / val2)))
        elif o == '*':
            num.append(str(val1 * val2))

    return hex(int(num.pop())).removeprefix('0x').upper()
