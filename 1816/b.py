import collections
import sys
from util import findints


Sample = collections.namedtuple('Sample', 'instruction before after')
Instruction = collections.namedtuple('Instruction', 'opcode a b c')

ALL_MNEMONICS = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']


def main():
    # Parse input
    text = open(sys.argv[1] if len(sys.argv) > 1 else 'in').read().strip()
    samples_text, program_text = (section.strip() for section in text.split('\n\n\n'))
    samples = [parse_sample(otext) for otext in samples_text.strip().split('\n\n')]
    program = [  # Parse program
        Instruction(*findints(line)) for line in program_text.strip().split('\n')
    ]

    # Analyze samples
    unidentified_mnemonics = ALL_MNEMONICS
    opcode_table = {}
    while unidentified_mnemonics:
        for sample in samples:
            possible_mnemonics = test_sample(sample, unidentified_mnemonics)
            if len(possible_mnemonics) == 1:
                mnemonic = possible_mnemonics[0]
                opcode = sample.instruction.opcode
                opcode_table[opcode] = mnemonic
                unidentified_mnemonics.remove(mnemonic)
                break

    # Run test program
    registers = (0, 0, 0, 0)
    for instruction in program:
        registers = execute_instruction(instruction, registers, opcode_table)
    print(registers[0])


def parse_sample(text):
    before_text, instruction_text, after_text = text.strip().splitlines()
    return Sample(
        instruction = Instruction(*findints(instruction_text)),
        before = tuple(findints(before_text)),
        after = tuple(findints(after_text)),
    )


def execute_instruction(instruction, registers, opcode_table):
    '''
    Run INSTRUCTION on REGISTERS (without mutating) and return the new register
    values.
    '''
    mnemonic = opcode_table[instruction.opcode]
    return execute_instruction_as(instruction, mnemonic, registers)


def execute_instruction_as(instruction, mnemonic, registers):
    '''
    Run INSTRUCTION (ignoring opcode, using MNEMONIC instead) on REGISTERS
    (without mutating) and return the new register values.
    '''
    registers = list(registers)

    _, a, b, c = instruction

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

    return tuple(registers)


def test_sample(sample, mnemonics):
    """
    >>> sample = parse_sample('''Before: [3, 2, 1, 1]
    ... 9 2 1 2
    ... After:  [3, 2, 2, 1]
    ... '''.strip())
    >>> test_sample(sample, ALL_MNEMONICS)
    ('addi', 'mulr', 'seti')
    """
    matches = []
    for mnemonic in mnemonics:
        expected_after = sample.after
        actual_after = execute_instruction_as(sample.instruction, mnemonic, sample.before)
        if expected_after == actual_after:
            matches.append(mnemonic)
    return tuple(matches)


if __name__ == '__main__':
    main()
