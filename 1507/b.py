from collections import namedtuple
from operator import and_, or_, invert, lshift, rshift


Instruction = namedtuple('Instruction', 'op args dest')


def main():
    # Parse puzzle input
    lines = open('in').read().strip().splitlines()
    lines.remove('44430 -> b')
    instructions = [parse(l) for l in lines]

    values = { 'b': 3176 }
    while instructions:
        # Find the first instruction that's ready to be run
        for inst in instructions:
            ready = all(
                isinstance(arg, int) or arg in values
                for arg in inst.args
            )
            if ready:
                break

        # Run it
        execute(inst, values)

        # Remove it so we don't try to run it again. Once every instruction
        # has been run, the loop ends.
        instructions.remove(inst)

    answer = values['a']
    print(answer)


def execute(inst, values):
    '''
    Execute INST, mutating VALUES
    '''
    functions = {
        'ID': lambda x: x,
        'AND': and_,
        'OR': or_,
        'NOT': invert,
        'LSHIFT': lshift,
        'RSHIFT': rshift,
    }
    f = functions[inst.op]
    args = tuple(
        arg if isinstance(arg, int) else values[arg]
        for arg in inst.args
    )
    result = f(*args)
    result &= 0xffff
    values[inst.dest] = result


def parse(line):
    expr, dest = line.split(' -> ')
    expr_parts = expr.split(' ')
    if len(expr_parts) == 3:
        arg1, op, arg2 = expr_parts
        args = [arg1, arg2]
    elif len(expr_parts) == 2:
        op, arg = expr_parts
        args = [arg]
    elif len(expr_parts) == 1:
        op = 'ID'
        args = [expr_parts[0]]
    else:
        assert False
    op = maybe_int(op)
    args = tuple(maybe_int(arg) for arg in args)
    dest = maybe_int(dest)
    return Instruction(op, args, dest)


def maybe_int(s):
    '''
    >>> maybe_int('1')
    1
    >>> maybe_int('x')
    'x'
    '''
    try:
        return int(s)
    except ValueError:
        return s


if __name__ == '__main__':
    main()
