from operator import add, sub, gt, lt, ge, le, eq, ne
from collections import defaultdict


def main():
    registers = defaultdict(int)
    highest = 0

    for line in open('in').read().strip().splitlines():
        reg, opname, value, _, condreg, condname, condvalue = [
            maybeint(n) for n in line.split()
        ]
        op = {
            'inc': add,
            'dec': sub,
        }[opname]
        cond = {
            '>': gt,
            '<': lt,
            '>=': ge,
            '<=': le,
            '==': eq,
            '!=': ne,
        }[condname]
        if cond(registers[condreg], condvalue):
            new_value = op(registers[reg], value)
            registers[reg] = new_value
            highest = max(highest, new_value)

    print(highest)


def maybeint(n):
    try:
        return int(n)
    except ValueError:
        return n


main()
