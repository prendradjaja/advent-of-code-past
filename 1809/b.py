import sys
import collections
import itertools
from util import findints


def main():
    text = open(sys.argv[1] if len(sys.argv) > 1 else 'in').read()
    players, marbles = findints(text)

    answer = play(players, marbles * 100)
    print(answer)


def play(players, marbles):
    '''
    >>> play(9, 25)
    32
    >>> play(10, 1618)
    8317
    >>> play(13, 7999)
    146373
    >>> play(17, 1104)
    2764
    >>> play(21, 6111)
    54718
    >>> play(30, 5807)
    37305
    '''
    buf = CircularBuffer()
    scores = collections.defaultdict(int)
    for marble, player in zip(
        range(1, marbles+1),
        itertools.cycle(range(1, players+1)),
    ):
        if marble % 23 != 0:
            buf.insert(marble)
        else:
            scores[player] += marble
            removed = buf.remove()
            scores[player] += removed
    return max(scores.values())


class ListNode:
    def __init__(self, value, next, prev):
        self.value = value
        self.next = next
        self.prev = prev


class CircularBuffer:
    def __init__(self):
        self.head = ListNode(0, None, None)
        self.head.next = self.head
        self.head.prev = self.head
        self.current = self.head

    def insert(self, value):
        '''
        >>> buf = CircularBuffer()
        >>> print(buf)
        (0)
        >>> buf.insert(1)
        >>> print(buf)
        0 (1)
        >>> buf.insert(2)
        >>> print(buf)
        0 (2) 1
        >>> buf.insert(3)
        >>> print(buf)
        0 2 1 (3)
        >>> buf.insert(4)
        >>> print(buf)
        0 (4) 2 1 3
        >>> buf.insert(5)
        >>> print(buf)
        0 4 2 (5) 1 3
        '''
        a = self.current.next
        b = self.current.next.next

        newnode = ListNode(value, b, a)
        a.next = newnode
        b.prev = newnode
        self.current = newnode

    def remove(self):
        '''
        >>> buf = CircularBuffer()
        >>> for n in range(1, 23):
        ...     buf.insert(n)
        >>> print(buf)
        0 16 8 17 4 18 9 19 2 20 10 21 5 (22) 11 1 12 6 13 3 14 7 15

        >>> buf.remove()
        9
        >>> print(buf)
        0 16 8 17 4 18 (19) 2 20 10 21 5 22 11 1 12 6 13 3 14 7 15
        '''
        node = self.current
        for _ in range(7):
            node = node.prev

        result = node.value

        a = node.prev
        b = node.next
        a.next = b
        b.prev = a

        self.current = b

        assert self.head is not node, 'TODO implement me'

        return result

    def __str__(self):
        itemstr = lambda node: f'{node.value} ' if node is not self.current else f'({node.value}) '
        result = itemstr(self.head)
        curr = self.head.next
        while curr is not self.head:
            result += itemstr(curr)
            curr = curr.next
        return result.strip()


if __name__ == '__main__':
    main()
