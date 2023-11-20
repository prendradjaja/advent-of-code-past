import sys


MY_PUZZLE_INPUT = 147061


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else MY_PUZZLE_INPUT
    target_subarray = [int(digit) for digit in str(n).zfill(5)]
    print(f'Using puzzle input {n}, i.e. looking for subarray {target_subarray}.')
    answer = play(target_subarray)
    print(answer)


def play(target_subarray):
    '''
    >>> play([5, 1, 5, 8, 9])
    9
    >>> play([0, 1, 2, 4, 5])
    5
    >>> play([9, 2, 5, 1, 0])
    18
    >>> play([5, 9, 4, 1, 4])
    2018
    '''
    items = [3, 7]
    p1 = 0
    p2 = 1
    while True:
        my_sum = items[p1] + items[p2]
        for digit in str(my_sum):
            items.append(int(digit))
        p1 = (p1 + 1 + items[p1]) % len(items)
        p2 = (p2 + 1 + items[p2]) % len(items)

        if items[-6:] == target_subarray:
            return len(items) - 6
        elif items[-7:-1] == target_subarray:
            print('Warning: Answer is in case 2')
            return len(items) - 7

        # if len(items) % 1000000 == 0:
        #     print(f'... {len(items):,}')


if __name__ == '__main__':
    main()
