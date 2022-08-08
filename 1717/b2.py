# Idea is from a hint from Reddit:
#     "What slows you down? It is the buffer manipulation. Do you need the
# buffer at all for this problem? Try to leverage your good news to mitigate
# the bad news."
# - https://www.reddit.com/r/adventofcode/comments/7kch29/2017_day_17_is_there_a_pattern_to_part_2/

STEPS = 301
INSERTIONS = 50000000


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


class ListNode:
    def __init__(self, value, next):
        self.value = value
        self.next = next


def main():
    buf = CircularBuffer()
    for n in range(1, INSERTIONS + 1):
        buf.advance(STEPS)
        buf.insert(n)
    print(buf.first_nonzero_item)


if __name__ == '__main__':
    main()
