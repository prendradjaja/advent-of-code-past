import sys
import collections
import re


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    rules, molecule = f.read().strip().split('\n\n')
    rules = parse_rules(rules)
    molecule = parse_molecule(molecule)

    generated = set()
    for i, atom in enumerate(molecule):
        for left, right in rules:
            if left == atom:
                generated.add(molecule[:i] + right + molecule[i+1:])

    print(len(generated))


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
