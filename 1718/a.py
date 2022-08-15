import sys
import string
from util import ints


def main():
    def get(value_or_register):
        if value_or_register in registers:
            return registers[value_or_register]
        return value_or_register

    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    program = [ints(line.split()) for line in lines]

    registers = { r: 0 for r in string.ascii_lowercase }
    ip = 0

    while 0 <= ip < len(program):
        instruction = program[ip]
        op, *args = instruction
        if op == 'snd':
            x = args[0]
            last_sound = get(x)
        elif op == 'set':
            x, y = args
            registers[x] = get(y)
        elif op == 'add':
            x, y = args
            registers[x] += get(y)
        elif op == 'mul':
            x, y = args
            registers[x] *= get(y)
        elif op == 'mod':
            x, y = args
            registers[x] %= get(y)
        elif op == 'rcv':
            x = args[0]
            if get(x):
                print(last_sound)
                exit()
        elif op == 'jgz':
            x, y = args
            if get(x):
                ip += get(y)
                continue
        else:
            1/0
        ip += 1


if __name__ == '__main__':
    main()
