STEPS = 301
INSERTIONS = 2017


class CircularBuffer:
    def __init__(self):
        self.node = ListNode(0, None)
        self.node.next = self.node

    def advance(self, steps):
        for _ in range(steps):
            self.node = self.node.next

    def insert(self, value):
        newnode = ListNode(value, self.node.next)
        self.node.next = newnode
        self.node = newnode


class ListNode:
    def __init__(self, value, next):
        self.value = value
        self.next = next


def main():
    buf = CircularBuffer()
    for n in range(1, INSERTIONS + 1):
        buf.advance(STEPS)
        buf.insert(n)
    print(buf.node.next.value)


if __name__ == '__main__':
    main()
