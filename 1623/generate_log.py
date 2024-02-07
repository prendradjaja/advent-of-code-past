from util import ints


def main():
    instructions = [ints(l.rstrip('\n').split()) for l in open('in')]
    registers = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
    run(instructions, registers)
    print('Part 1:       ', registers['a'])


def run(instructions, registers):
    '''
    Warning: Mutates `instructions` AND `registers`!

    Run the program (instructions) on the given registers.
    '''
    time = 0
    ip = 0
    print('time ip op args a b c d'.replace(' ', '\t'))
    print(time, '', '', '', *registers.values(), sep='\t')
    while ip < len(instructions):
        time += 1
        toggle_description = ''
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
                    toggle_description = 'toggle skipped: attempted to toggle an insturction outside the program'
                    skip = True
                if not skip:
                    old_op = instruction_to_toggle[0]
                    old_instruction = instruction_to_toggle[:]
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
                    toggle_description = f'toggle: at address {idx}, {to_str(old_instruction)} became {to_str(instruction_to_toggle)}'
            else:
                1/0
        except (NotARegisterException, NotANumberException) as e:
            print('Warning: Invalid instruction', instructions[ip])
            pass  # Invalid instructions are to be skipped

        print(time, ip, op, ' '.join(str(each) for each in args), *registers.values(), toggle_description, sep='\t')

        ip += offset


class NotARegisterException(Exception):
    pass


class NotANumberException(Exception):
    pass


def to_str(instruction):
    return ' '.join(str(x) for x in instruction)


def assert_is_register_name(dst):
    if dst not in set('abcd'):
        raise NotARegisterException()


def assert_is_number(n):
    if not isinstance(n, int):
        raise NotANumberException()


if __name__ == '__main__':
    main()
