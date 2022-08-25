from util import consecutives
import sys


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    polymer = f.read().strip()

    # A hack. Explanation: Try removing this line, and you'll see a null
    # error. My part 1 solution had some edge case problem (the literal edge
    # of the list -- i.e. the beginning or end of the list) that didn't matter
    # for part 1, but that do matter now. Maybe can be solved with a sentinel
    # node list implementation? Easier: Just add extra non-reactive characters
    # to the start and end of the polymer. :)
    polymer = '~' + polymer + '~'

    letters = set(polymer.lower())
    answer = (
        min(fully_react(remove(polymer, letter)) for letter in letters)
        - 2  # Don't count the ~s
    )
    print(answer)


def remove(polymer, letter):
    variants = [letter.lower(), letter.upper()]
    return ''.join(ch for ch in polymer if ch not in variants)


def fully_react(polymer_string):
    polymer = list_from_sequence(polymer_string)
    node = polymer
    while node:
        node = react_at(node)
    return length(polymer)


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


def nodes(head, start):
    node = start
    while node:
        yield node
        node = node.next
    node = head
    while node is not start:
        yield node
        node = node.next


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
