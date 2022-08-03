import sys


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    program = [l.rstrip('\n') for l in f]

    print('Part 1 answer:', run(program, {'a': 0, 'b': 0})['b'])
    print('Part 2 answer:', run(program, {'a': 1, 'b': 0})['b'])


def run(program, registers):
    ip = 0

    while 0 <= ip < len(program):
        instruction = program[ip]
        op, args = instruction.split(' ', maxsplit=1)
        if op == 'hlf':
            r = args
            assert registers[r] % 2 == 0
            registers[r] //= 2
            ip += 1
        elif op == 'tpl':
            r = args
            registers[r] *= 3
            ip += 1
        elif op == 'inc':
            r = args
            registers[r] += 1
            ip += 1
        elif op == 'jmp':
            offset = int(args)
            offset = int(offset)
            ip += offset
        elif op == 'jie':
            r, offset_str = args.split(', ')
            offset = int(offset_str)
            if registers[r] % 2 == 0:
                ip += offset
            else:
                ip += 1
        elif op == 'jio':
            r, offset_str = args.split(', ')
            offset = int(offset_str)
            if registers[r] == 1:
                ip += offset
            else:
                ip += 1

    return registers


if __name__ == '__main__':
    main()
