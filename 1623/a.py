# import fileinput, collections, collections as cl, itertools, itertools as it, math, random, sys, re, string, functools
# from gridlib import gridsource as gridlib, gridcustom # *, gridsource, gridcardinal, gridplane
# from util import *

import sys
from util import ints


def main():

    # # Slow-ish: Takes ~0.5 seconds
    # instructions = [ints(l.rstrip('\n').split()) for l in open('day12input.txt')]
    # registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    # run(instructions, registers)
    # print('Day 12 part 1:', registers['a'])
    # assert registers['a'] == 318007

    # # Slow: Takes ~10 seconds
    # instructions = [ints(l.rstrip('\n').split()) for l in open('day12input.txt')]
    # registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    # run(instructions, registers)
    # print('Day 12 part 2:', registers['a'])
    # assert registers['a'] == 9227661

    instructions = [ints(l.rstrip('\n').split()) for l in open('ex')]
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    run(instructions, registers)
    print('Example:      ', registers['a'])
    assert registers['a'] == 3

    instructions = [ints(l.rstrip('\n').split()) for l in open('in')]
    registers = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
    run(instructions, registers)
    print('Part 1:       ', registers['a'])
    assert registers['a'] == 13776



def run(instructions, registers):
    '''
    Warning: Mutates `instructions` AND `registers`!

    Run the program (instructions) on the given registers.
    '''
    n = 0
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
                if isinstance(jumpoffset, str):
                    assert_is_register_name(jumpoffset)
                    jumpoffset = registers[jumpoffset]

                if isinstance(cond, str):
                    isjump = registers[cond] != 0
                else:
                    isjump = cond != 0
                if isjump:
                    offset = jumpoffset
            elif op == 'tgl':
                reg = args[0]
                assert_is_register_name(reg)
                idx = ip + registers[reg]
                try:
                    instruction_to_toggle = instructions[idx]
                    skip = False
                except IndexError:
                    skip = True
                if not skip:
                    old_op = instruction_to_toggle[0]
                    new_op = {
                        # For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
                        'inc': 'dec',
                        'dec': 'inc',
                        'tgl': 'inc',

                        # For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
                        'jnz': 'cpy',
                        'cpy': 'jnz',
                    }[old_op]
                    instruction_to_toggle[0] = new_op
            else:
                1/0
        except (NotARegisterException, NotANumberException) as e:
            print('Warning: Invalid instruction', instructions[ip])
            pass  # Invalid instructions are to be skipped

        # print(registers['a'], registers['b'], registers['c'], registers['d'])
        # for i, each in enumerate(instructions):
        #     print('-' if i == ip else ' ', each)
        # print()

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
