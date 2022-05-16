import sys
import collections


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    rules, molecule = f.read().strip().split('\n\n')
    rules = parse_rules(rules)

    generated = set()
    for left, rights in rules.items():
        for i in range(molecule.count(left)):
            for right in rights:
                generated.add(replace_nth(molecule, left, right, i))

    print(len(generated))


def parse_rules(rules):
    result = collections.defaultdict(list)
    for line in rules.splitlines():
        left, right = line.split(' => ')
        result[left].append(right)
    return result


def replace_nth(s, old, new, n):
    '''
    Replace the "N"th occurrence (zero-indexed) of OLD in S with NEW

    >>> replace_nth('the box of the fish in the pond', 'the', 'a', 1)
    'the box of a fish in the pond'
    >>> replace_nth('the box of the fish in the pond', 'the', 'a', 0)
    'a box of the fish in the pond'
    >>> replace_nth('the box of the fish in the pond', 'the', 'a', 2)
    'the box of the fish in a pond'
    '''
    n = n + 1

    assert s.count(old) >= n

    PLACEHOLDER = '%'
    assert PLACEHOLDER not in s
    assert PLACEHOLDER not in old
    assert PLACEHOLDER not in new

    s = s.replace(old, PLACEHOLDER, n)
    s = s.replace(PLACEHOLDER, old, n-1)
    s = s.replace(PLACEHOLDER, new)

    return s


if __name__ == '__main__':
    main()
