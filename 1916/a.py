import sys
import itertools

from util import listify, strjoin


def main():
    text = open(sys.argv[1] if len(sys.argv) > 1 else 'in').read().strip()
    lst = [int(digit) for digit in text]
    for _ in range(100):
        lst = fft(lst)
    answer = strjoin(lst[:8], '')
    print(answer)


@listify
def fft(lst):
    for i in range(1, len(lst)+1):
        total = sum(a * b for a, b in zip(lst, pattern(i)))
        yield abs(total) % 10


def pattern(which_digit):
    items = (
        [0] * which_digit +
        [1] * which_digit +
        [0] * which_digit +
        [-1] * which_digit
    )
    result = itertools.cycle(items)
    next(result)  # skip first value
    return result


if __name__ == '__main__':
    main()
