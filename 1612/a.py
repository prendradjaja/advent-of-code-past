import sys
from util import ints


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    instructions = [ints(line.split()) for line in lines]

    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    ip = 0
    while ip < len(instructions):
        assert ip >= 0

        op, *args = instructions[ip]
        offset = 1
        if op == 'cpy':
            src, dst = args
            if isinstance(src, str):
                registers[dst] = registers[src]
            else:
                registers[dst] = src
        elif op == 'inc':
            dst = args[0]
            registers[dst] += 1
        elif op == 'dec':
            dst = args[0]
            registers[dst] -= 1
        elif op == 'jnz':
            cond, jumpoffset = args
            assert not isinstance(jumpoffset, str)
            if isinstance(cond, str):
                isjump = registers[cond] != 0
            else:
                isjump = cond != 0
            if isjump:
                offset = jumpoffset
        else:
            1/0

        ip += offset

    print(registers['a'])


if __name__ == '__main__':
    main()
