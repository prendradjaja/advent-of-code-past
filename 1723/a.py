import sys
from util import ints


def main():
    def get(value_or_register):
        if value_or_register in registers:
            return registers[value_or_register]
        return value_or_register

    f = open(sys.argv[1])
    lines = [l.rstrip('\n') for l in f]
    program = [ints(line.split()) for line in lines]

    registers = { r: 0 for r in 'abcdefgh' }
    registers['a'] = 1
    time = 0
    ip = 0

    # registers = dict(zip('abcdefgh', [1, 108400, 125400, 2, 54202, 0, -54198, 0]))
    # time = 433611
    # ip = 11
    # for _ in range(54195):
    #     time += 8
    #     registers['e'] += 1

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
        elif op == 'mydivis':
            if (
                registers['b'] % registers['d'] == 0
                and registers['b'] // registers['d'] >= registers['e']
            ):
                registers['f'] = 0
        elif op == 'noop':
            pass
        else:
            1/0

        print(time, ip, op, x, y, *registers.values(), sep='\t')

        ip = next_ip

    print('Done')


if __name__ == '__main__':
    main()
