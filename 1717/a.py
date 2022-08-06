import sys


STEP_COUNT = 301

INSERTION_COUNT = 2017


class CircularBuffer:
    def __init__(self):
        self.items = [0]
        self.current_position = 0

    def advance(self):
        self.current_position = (self.current_position + STEP_COUNT) % len(self.items)

    def insert(self, value):
        self.items[self.current_position + 1 : ] = (
            [value]
            + self.items[self.current_position + 1 : ]
        )
        self.current_position += 1

    def __str__(self):
        result = ''
        for i, item in enumerate(self.items):
            if i != self.current_position:
                result += f'{item} '
            else:
                result += f'({item}) '
        return result

    def get(self, index):
        return self.items[index % len(self.items)]


def main():
    buf = CircularBuffer()
    for n in range(1, INSERTION_COUNT+1):
        buf.advance()
        buf.insert(n)
    print(buf.get(buf.current_position + 1))


if __name__ == '__main__':
    main()
