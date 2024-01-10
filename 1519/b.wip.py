#!./env/bin/python3
'''
Usage example:
    ./b.wip.py med
'''

import astar

import sys
import collections
import re
import functools

from analyze import analyze


def main():
    global visited
    visited = set()

    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    rules, molecule = f.read().strip().split('\n\n')
    rules = parse_rules(rules)
    molecule = parse_molecule(molecule)

    inert_elements = analyze(rules)

    just_one_electron = ('e',)

    path = list(astar.find_path(
        just_one_electron,
        molecule,
        neighbors_fnct = lambda node: neighbors(rules, node),
        heuristic_cost_estimate_fnct = lambda node1, node2: heuristic(inert_elements, node1, node2),
    ))
    assert path[-1] == molecule
    print('Nodes visited:')
    print(len(visited))
    print('Answer:')
    print(len(path) - 1)


def neighbors(rules, node):
    visited.add(node)
    molecule = node
    for i, atom in enumerate(molecule):
        for left, right in rules:
            if left == atom:
                yield molecule[:i] + right + molecule[i+1:]


def heuristic(inert_elements, curr_node, goal_node):
    curr_counts = collections.Counter(curr_node)
    goal_counts = collections.Counter(goal_node)
    for each in inert_elements:
        if curr_counts[each] > goal_counts[each]:
            return float('inf')
    return 1


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
