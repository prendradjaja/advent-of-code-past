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

    registers = dict(zip('abcdefgh', [1, 108400, 125400, 2, 2, 1, 0, 0]))
    time = 10
    ip = 11
    print('time ip op x y a b c d e f g h'.replace(' ', '\t'))
    print(time, '', '', '', '', *registers.values(), sep='\t')
    while 0 <= ip < len(program):
        next_ip = ip + 1
        time += 1
        instruction = program[ip]
        op, x, y = instruction
        if op == 'set':
            registers[x] = get(y)
        elif op == 'sub':
            registers[x] -= get(y)
        elif op == 'mul':
            registers[x] *= get(y)
        elif op == 'jnz':
            if get(x) != 0:
                next_ip = ip + get(y)
        else:
            1/0

        print(time, ip, op, x, y, *registers.values(), sep='\t')

        ip = next_ip


if __name__ == '__main__':
    main()
