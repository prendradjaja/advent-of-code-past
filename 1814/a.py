import sys


MY_PUZZLE_INPUT = 147061


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else MY_PUZZLE_INPUT
    print(f'Making {n} + 10 recipes. Answer:')
    answer = play(n)
    print(answer)


def play(n):
    '''
    >>> play(9)
    '5158916779'
    '''
    target_length = n + 10
    items = [3, 7]
    p1 = 0
    p2 = 1
    while len(items) < target_length:
        my_sum = items[p1] + items[p2]
        for digit in str(my_sum):
            items.append(int(digit))
        p1 = (p1 + 1 + items[p1]) % len(items)
        p2 = (p2 + 1 + items[p2]) % len(items)
    return ''.join(str(score) for score in items[n : target_length])


if __name__ == '__main__':
    main()
