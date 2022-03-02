import collections
from datetime import datetime

from progress import ProgressBar


n = 5
n = 3012210


def main():
    elves = LinkedList(range(1, n+1), verbose=True)
    print('Simulating...')
    progress = ProgressBar(n)

    while len(elves) > 1:
        first = elves.popleft()
        elves.popleft()
        elves.append(first)
        if len(elves) % 1123 == 0:
            progress.show(n - len(elves))

    progress.done()

    print('\nAnswer:')
    print(elves[0])


class LinkedList:
    def __init__(self, lst, /, verbose=False):
        '''
        Create a LinkedList from a list.
        '''
        if verbose:
            print('Initializing LinkedList...')
            progress = ProgressBar(len(lst))

        first = LinkedListNode(lst[0])
        prev = first
        for i, x in enumerate(lst[1:]):
            curr = LinkedListNode(x)
            curr.prev = prev
            prev.next = curr
            prev = curr

            if verbose and i % 1123 == 0:
                progress.show(i)
        if verbose:
            progress.done()

        self.first = first
        self.last = prev
        self.length = len(lst)

        # Initialize center
        center_index = len(lst) // 2
        i = 0
        node = self.first
        while i < center_index:
            i += 1
            node = node.next
        self.center = node


    def __len__(self):
        return self.length


    def __str__(self):
        node = self.first
        result = '[ '
        while node:
            result += f'{node.value} '
            node = node.next
        result += ']'
        return result


    def __getitem__(self, index):
        assert index == 0
        return self.first.value


    def popleft(self):
        dropped = self.first
        self.first = self.first.next
        self.length -= 1

        if self.length:
            self.first.prev = None
            if self.length % 2 == 0:
                self.center = self.center.next
        else:
            self.last = None
            self.center = None

        return dropped.value


    def popcenter(self):
        assert self.length > 0

        dropped = self.center
        left = self.center.prev
        right = self.center.next

        if left and right:
            left.next = right
            right.prev = left
            self.length -= 1

            if self.length % 2 == 0:
                self.center = right
            else:
                self.center = left

        elif left and not right:
            assert self.length == 2
            self.last = left
            left.next = None
            self.center = left
            self.length -= 1

        elif not left and not right:
            assert self.length == 1
            self.first = None
            self.last = None
            self.center = None
            self.length -= 1

        else:
            raise Exception('Invalid state')

        return dropped.value


    def append(self, item):
        node = LinkedListNode(item)

        if self.length:
            node.prev = self.last
            self.last.next = node
            self.last = node
            self.length += 1

            if self.length % 2 == 0:
                self.center = self.center.next

        else:
            self.first = node
            self.last = node
            self.length = 1
            self.center = node


class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


if __name__ == '__main__':
    main()
