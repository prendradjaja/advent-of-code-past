'''
This approach will work for the example input, but not the puzzle input -- too
many possibilities to search exhaustively via DFS
'''

import sys
import collections
from util import findints


Component = collections.namedtuple('Component', 'left right id')


def main():
    def dfs(u, visited):
        # Visit
        u_ids = [comp.id for comp in u]
        print(f'Strength: {strength(u_ids)}\t{u_ids}')

        # Continue search
        visited.add(u)
        for v in neighbors(u):
            if v not in visited:
                dfs(v, visited)

    def neighbors(u):
        u_ids = [comp.id for comp in u]
        unused = [comp for comp in all_components if comp.id not in u_ids]
        pins = u[-1].right if u else 0
        for comp in unused:
            if comp.left == pins:
                yield u + (comp,)
            if comp.right == pins:
                yield u + (reverse(comp),)


    # Parse puzzle input
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    assert len(set(lines)) == len(lines)  # i.e. all components are unique
    all_components = []
    for line in lines:
        left, right = findints(line)
        all_components.append(
            Component(left, right, line)
        )

    # Search
    dfs((), set())


def reverse(component):
    return Component(
        component.right,
        component.left,
        component.id
    )


def strength(bridge):
    '''
    >>> strength(['0/1', '10/1', '9/10'])
    31
    '''
    result = 0
    for component_id in bridge:
        left, right = findints(component_id)
        result += left + right
    return result


if __name__ == '__main__':
    main()
