import sys
import itertools
from util import ints


SAMPLE_SIZE = 10


def main():
    f = open('./in')
    lines = [l.rstrip('\n') for l in f]
    program = [ints(line.split()) for line in lines]

    expected = [0, 1] * (SAMPLE_SIZE // 2)
    for a_value in itertools.count(1):
        registers = {'a': a_value, 'b': 0, 'c': 0, 'd': 0}
        output_values = run(program, registers)
        if expected == list(itertools.islice(output_values, SAMPLE_SIZE)):
            break

    print(a_value)


def run(program, registers):
    '''
    Run PROGRAM, mutating REGISTERS.

    Yields values from "out" instructions.
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
        elif op == 'out':
            [arg] = args
            if isinstance(arg, str):
                yield registers[arg]
            else:
                yield arg
        else:
            1/0

        ip += offset


if __name__ == '__main__':
    main()
