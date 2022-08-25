import sys
import collections

from util import listify


def main():
    global parent, children

    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]

    parent = {}
    children = collections.defaultdict(list)
    for line in lines:
        p, c = line.split(')')
        parent[c] = p
        children[p].append(c)

    you_ancestors = ancestors('YOU')
    san_ancestors = ancestors('SAN')
    for each in you_ancestors:
        if each in san_ancestors:
            common_ancestor = each
            break
    else:
        assert False

    answer = you_ancestors.index(common_ancestor) + san_ancestors.index(common_ancestor) - 2
    print(answer)


@listify
def ancestors(node):
    while not is_root(node):
        yield node
        node = parent[node]


def is_root(node):
    return node not in parent


if __name__ == '__main__':
    main()
