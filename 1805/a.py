from util import consecutives
import sys


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    polymer = f.read().strip()

    polymer = list_from_sequence(polymer)
    node = polymer
    while node:
        node = react_at(node)
    print(length(polymer))


def react_at(node):
    '''
    Tries to react two units at the current node. May perform multiple
    cascading reactions.

    Whether or not any reaction is performed, return the next node to continue
    iterating from.
    '''
    if not node.next:
        return None
    A = node
    B = node.next
    a = A.value
    b = B.value
    if a != b and a.lower() == b.lower():
        Z = A.prev
        C = B.next
        Z.next = C
        C.prev = Z
        return react_at(Z)
    else:
        return B


class ListNode:
    def __init__(self, value, next, prev):
        self.value = value
        self.next = next
        self.prev = prev


def list_from_sequence(seq):
    nodes = [ListNode(value, None, None) for value in seq]
    for a, b in consecutives(nodes):
        a.next = b
        b.prev = a
    return nodes[0]


def length(lst):
    result = 0
    while lst:
        result += 1
        lst = lst.next
    return result


if __name__ == '__main__':
    main()
