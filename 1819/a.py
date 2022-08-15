import collections
import sys
from util import ints, findint


Instruction = collections.namedtuple('Instruction', 'mnemonic a b c')


def main():
    # Parse ip declaration
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    first_line = f.readline()
    assert '#ip' in first_line
    ip_register = findint(first_line)

    # Parse the rest of the program
    program = [
        Instruction(*ints(line.split())) for line in f.read().splitlines()
    ]

    # Run the program and print the answer
    registers = [0, 0, 0, 0, 0, 0]
    while 0 <= registers[ip_register] < len(program):
        instruction = program[registers[ip_register]]
        execute_instruction(instruction, registers)
        registers[ip_register] += 1

    print(registers[0])


def execute_instruction(instruction, registers):
    '''
    Run INSTRUCTION, which mutates REGISTERS.
    '''
    mnemonic, a, b, c = instruction

    if mnemonic == 'addr':
        registers[c] = registers[a] + registers[b]
    elif mnemonic == 'addi':
        registers[c] = registers[a] + b

    elif mnemonic == 'mulr':
        registers[c] = registers[a] * registers[b]
    elif mnemonic == 'muli':
        registers[c] = registers[a] * b

    elif mnemonic == 'banr':
        registers[c] = registers[a] & registers[b]
    elif mnemonic == 'bani':
        registers[c] = registers[a] & b

    elif mnemonic == 'borr':
        registers[c] = registers[a] | registers[b]
    elif mnemonic == 'bori':
        registers[c] = registers[a] | b

    elif mnemonic == 'setr':
        registers[c] = registers[a]
    elif mnemonic == 'seti':
        registers[c] = a

    elif mnemonic == 'gtir':
        registers[c] = int(a > registers[b])
    elif mnemonic == 'gtri':
        registers[c] = int(registers[a] > b)
    elif mnemonic == 'gtrr':
        registers[c] = int(registers[a] > registers[b])

    elif mnemonic == 'eqir':
        registers[c] = int(a == registers[b])
    elif mnemonic == 'eqri':
        registers[c] = int(registers[a] == b)
    elif mnemonic == 'eqrr':
        registers[c] = int(registers[a] == registers[b])

    else:
        assert False


if __name__ == '__main__':
    main()
