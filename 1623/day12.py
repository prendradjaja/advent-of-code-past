import sys
from util import ints


def main():
    f = open('day12input.txt')
    lines = [l.rstrip('\n') for l in f]
    instructions = [ints(line.split()) for line in lines]

    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    run(instructions, registers)
    print('Part 1 answer:', registers['a'])
    assert registers['a'] == 318007

    # registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    # run(instructions, registers)
    # print('Part 2 answer:', registers['a'])
    # assert registers['a'] == 9227661


def run(instructions, registers):
    '''
    Warning: Mutates `registers`!

    Run the program (instructions) on the given registers.
    '''
    ip = 0
    while ip < len(instructions):
        assert ip >= 0

        op, *args = instructions[ip]
        offset = 1
        try:
            if op == 'cpy':
                src, dst = args
                if isinstance(src, str):
                    registers[dst] = registers[src]
                else:
                    assert_is_register_name(dst)
                    registers[dst] = src
            elif op == 'inc':
                dst = args[0]
                assert_is_register_name(dst)
                registers[dst] += 1
            elif op == 'dec':
                dst = args[0]
                assert_is_register_name(dst)
                registers[dst] -= 1
            elif op == 'jnz':
                cond, jumpoffset = args
                assert_is_number(jumpoffset)
                if isinstance(cond, str):
                    isjump = registers[cond] != 0
                else:
                    isjump = cond != 0
                if isjump:
                    offset = jumpoffset
            else:
                1/0
        except (NotARegisterException, NotANumberException) as e:
            print('Warning: Invalid instruction')
            pass  # Invalid instructions are to be skipped

        ip += offset


class NotARegisterException(Exception):
    pass


class NotANumberException(Exception):
    pass


def assert_is_register_name(dst):
    if dst not in set('abcd'):
        raise NotARegisterException()


def assert_is_number(n):
    if not isinstance(n, int):
        raise NotANumberException()



if __name__ == '__main__':
    main()
