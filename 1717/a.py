STEPS = 301
INSERTIONS = 2017


class CircularBuffer:
    def __init__(self):
        self.items = [0]
        self.current_position = 0

    def advance(self, steps):
        self.current_position = (self.current_position + steps) % len(self.items)

    def insert(self, value):
        self.items[self.current_position + 1 : ] = (
            [value]
            + self.items[self.current_position + 1 : ]
        )
        self.current_position += 1

    def get(self, index):
        return self.items[index % len(self.items)]


def main():
    buf = CircularBuffer()
    for n in range(1, INSERTIONS + 1):
        buf.advance(STEPS)
        buf.insert(n)
    print(buf.get(buf.current_position + 1))


if __name__ == '__main__':
    main()
