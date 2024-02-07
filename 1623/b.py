'''
The problem description hints somewhat strongly towards the approach I used:

- Inspect the program given. See generate_log.py -- I used a similar program,
  though not exactly that one. I pasted the output into a spreadsheet, where
  the "group rows" in Google Sheets was helpful.
- Spreadsheet: https://docs.google.com/spreadsheets/d/1BoxtN_X2O55B4LNOyumQqQsR4QCl7ifPoU18e-ZjOaM/edit#gid=0

- The key observation was noticing an addition loop early in the program (and
  that loop is itself inside a multiplication loop).
- In my input, the multiplication loop is lines 5-10. It is equivalent to this
  pseudocode: "reg_a = reg_b * reg_c; reg_c = 0; reg_d = 0"
- One other important observation was that the "tgl" instruction was only used
  a few times, suggesting that it might not be something we need to worry
  about. (In fact, the first toggle happens after the multiplication loop, so
  we indeed don't need to worry about it.)

- Having found this loop, we simply extend the capabilities of the assembunny
  language to add a multiplication instruction and edit the program accodingly
  (compare the file "in" to "in-optimized"), and it will run to completion
  much more quickly.
'''

from util import ints


def main():
    instructions = [ints(l.rstrip('\n').split()) for l in open('in-optimized')]
    registers = {'a': 12, 'b': 0, 'c': 0, 'd': 0}
    run(instructions, registers)
    print(registers['a'])



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
            elif op == 'noop':
                pass
            elif op == 'inc':
                dst = args[0]
                assert_is_register_name(dst)
                registers[dst] += 1
            elif op == 'mul':
                src1, src2, dst = args
                assert_is_register_name(src1)
                assert_is_register_name(src2)
                assert_is_register_name(dst)
                registers[dst] += registers[src1] * registers[src2]
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
