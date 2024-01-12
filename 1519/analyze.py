
import sys
import collections
import re


def main():
    print('Analyzing puzzle input.\n')
    rules, _ = open('./in').read().strip().split('\n\n')
    rules = parse_rules(rules)
    analyze(rules, True)


def analyze(rules, verbose=False):
    lefts = [left for left, right in rules]
    assert all(is_atom(each) for each in lefts)
    if verbose:
        print('Every left side consists of one atom (an atom is "e" or a capital letter')
        print('followed by 0 or more lowercase letters)')

    assert all(
        len(right) > 1
        or (left == 'e' and len(right) >= 1)
        for left, right in rules
    )
    if verbose:
        print('\nEvery replacement strictly increases the size of the molecule')

    elements = set(lefts) | {atom for left, right in rules for atom in right}
    if verbose:
        print(f'\nThere are {len(elements)} different elements that appear in the rules. They are:')
        print(*sorted(elements))

    inert_elements = [each for each in elements if each not in lefts]
    if verbose:
        print(f'\nOf those, {len(inert_elements)} are "inert", i.e. they do not appear on the left side of any rule.')
        print('They are:')
        print(*sorted(inert_elements))

    # TODO check no element is called E

    return inert_elements


def is_atom(s):
    if s == 'e':
        return True
    elif len(s) == 1 and s.isupper():
        return True
    elif len(s) > 1 and s[0].isupper() and s[1:].islower():
        return True
    else:
        return False


def countupper(s):
    return sum(1 for ch in s if ch.isupper())


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
