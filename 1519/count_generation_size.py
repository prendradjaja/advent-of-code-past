import sys
import collections
import re


def main():
    n = int(sys.argv[1])
    rules, molecule = open('./in').read().strip().split('\n\n')
    rules = parse_rules(rules)
    molecule = parse_molecule(molecule)

    just_one_electron = ('e',)

    curr_generation = [just_one_electron]
    for _ in range(n):
        curr_generation = get_next_generation(curr_generation, rules)
    print(len(curr_generation))



def get_next_generation(curr_generation, rules):
    generated = set()
    for molecule in curr_generation:
        for i, atom in enumerate(molecule):
            for left, right in rules:
                if left == atom:
                    generated.add(molecule[:i] + right + molecule[i+1:])
    return generated


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
