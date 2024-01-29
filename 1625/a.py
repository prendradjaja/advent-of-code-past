import sys
from util import ints


def main():
    f = open('./day12input.txt')
    lines = [l.rstrip('\n') for l in f]
    program = [ints(line.split()) for line in lines]

    registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    run(program, registers)
    print(registers)


def run(program, registers):
    '''
    Run PROGRAM, mutating REGISTERS. Returns REGISTERS.
    '''
    ip = 0
    while ip < len(program):
        assert ip >= 0

        op, *args = program[ip]
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

    return registers


if __name__ == '__main__':
    main()
