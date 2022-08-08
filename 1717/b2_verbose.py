# Just for fun: Visualizing what b2's algorithm looks like :)

# Example input
STEPS = 3
INSERTIONS = 9


class CircularBuffer:
    def __init__(self):
        self.first_nonzero_item = None
        self.current_position = 0
        self.length = 1

    def advance(self, steps):
        self.current_position = (self.current_position + steps) % self.length

    def insert(self, value):
        self.current_position += 1
        self.length += 1
        if self.current_position == 1:
            self.first_nonzero_item = value

    def __str__(self):
        result = ''
        for n in range(self.length):
            if n == 0:
                value = str(0)
            elif n == 1:
                value = str(self.first_nonzero_item)
            else:
                value = '?'

            if n == self.current_position:
                value = '(' + value + ')'

            result += value + ' '
        return result


class ListNode:
    def __init__(self, value, next):
        self.value = value
        self.next = next


def main():
    buf = CircularBuffer()
    print(buf)
    for n in range(1, INSERTIONS + 1):
        buf.advance(STEPS)
        buf.insert(n)
        print(buf)


if __name__ == '__main__':
    main()
