import sys
import collections
import itertools
from util import findints


def main():
    text = open(sys.argv[1] if len(sys.argv) > 1 else 'in').read()
    players, marbles = findints(text)

    answer = play(players, marbles)
    print(answer)

    # Part 2: I guess it's too slow -- probably use a linked list. TODO


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


class CircularBuffer:
    def __init__(self):
        self.items = [0]
        self.current_index = 0

    def insert(self, value):
        '''
        >>> buf = CircularBuffer()
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
        index = (self.current_index + 1) % len(self.items)
        insert_after(self.items, index, value)
        self.current_index = index + 1

    def remove(self):
        '''
        >>> buf = CircularBuffer()
        >>> buf.items = [0, 16, 8, 17, 4, 18, 9, 19, 2, 20, 10, 21, 5, 22, 11, 1, 12, 6, 13, 3, 14, 7, 15]
        >>> buf.current_index = 13
        >>> print(buf)
        0 16 8 17 4 18 9 19 2 20 10 21 5 (22) 11 1 12 6 13 3 14 7 15
        >>> buf.remove()
        9
        >>> print(buf)
        0 16 8 17 4 18 (19) 2 20 10 21 5 22 11 1 12 6 13 3 14 7 15

        >>> buf = CircularBuffer()
        >>> buf.items = [0, 1, 2, 3, 4, 5, 6, 7]
        >>> buf.current_index = 6
        >>> buf.remove()
        7
        >>> print(buf)
        (0) 1 2 3 4 5 6
        '''
        index = (self.current_index - 7) % len(self.items)
        result = self.items.pop(index)
        if index == len(self.items):
            index = 0
        assert 0 <= index < len(self.items)
        self.current_index = index
        return result

    def __str__(self):
        result = ''
        for i, n in enumerate(self.items):
            if i == self.current_index:
                result += f'({n}) '
            else:
                result += f'{n} '
        return result.strip()


def insert_after(lst, index, value):
    '''
    >>> xs = ['a', 'b', 'c', 'd']
    >>> insert_after(xs, 0, 'A')
    >>> xs
    ['a', 'A', 'b', 'c', 'd']
    >>> insert_after(xs, 2, 'B')
    >>> xs
    ['a', 'A', 'b', 'B', 'c', 'd']
    >>> insert_after(xs, 5, 'Z')
    >>> xs
    ['a', 'A', 'b', 'B', 'c', 'd', 'Z']
    '''
    assert 0 <= index < len(lst)
    lst[index+1 : index+1] = [value]


if __name__ == '__main__':
    main()
