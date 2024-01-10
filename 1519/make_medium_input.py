'''
Usage example:

    python3 make_medium_input.py 5 > med
'''

import sys
import collections
import re
import random

from analyze import analyze


def main():
    n = int(sys.argv[1])
    raw_rules, _ = open('./in').read().strip().split('\n\n')
    rules = parse_rules(raw_rules)

    inert_elements = analyze(rules)

    molecule = ('e',)
    for _ in range(n):
        # Pick a random non-inert atom to replace
        idx = random.choice([
            i
            for i, atom in enumerate(molecule)
            if atom not in inert_elements
        ])
        atom = molecule[idx]

        # Pick a random rule to apply
        replacement = random.choice([
            each
            for each in rules
            if each[0] == atom
        ])[1]
        molecule = molecule[:idx] + replacement + molecule[idx+1:]

    print(raw_rules)
    print()
    print(''.join(molecule))


def parse_molecule(molecule):
    '''
    >>> parse_molecule('e')
    ('e',)
    >>> parse_molecule('HeH')
    ('He', 'H')
    >>> parse_molecule('HOH')
    ('H', 'O', 'H')
    '''
    return tuple(
        re.sub(r'[A-Z]', r' \g<0>', molecule)  # Add a space before every capital letter
        .split()
    )


def parse_rules(rules):
    result = []
    for line in rules.splitlines():
        left, right = line.split(' => ')
        right = parse_molecule(right)
        result.append((left, right))
    return result


if __name__ == '__main__':
    main()
