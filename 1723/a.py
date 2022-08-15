import sys
from util import ints


def main():
    def get(value_or_register):
        if value_or_register in registers:
            return registers[value_or_register]
        return value_or_register

    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    program = [ints(line.split()) for line in lines]

    registers = { r: 0 for r in 'abcdefgh' }
    ip = 0
    multiplications = 0
    while 0 <= ip < len(program):
        instruction = program[ip]
        op, x, y = instruction
        if op == 'set':
            registers[x] = get(y)
        elif op == 'sub':
            registers[x] -= get(y)
        elif op == 'mul':
            registers[x] *= get(y)
            multiplications += 1
        elif op == 'jnz':
            if get(x) != 0:
                ip += get(y)
                continue
        else:
            1/0
        ip += 1

    print(multiplications)


if __name__ == '__main__':
    main()
