from functools import reduce
from operator import xor


LIST_SIZE = 256


def main():
    answer = knot_hash('183,0,31,146,254,240,223,150,2,206,161,1,255,232,199,88')
    print(answer)


def reverse(lst, current_position, length):
    '''
    >>> reverse([0, 1, 2, 3, 4], 0, 3)
    [2, 1, 0, 3, 4]
    >>> reverse([2, 1, 0, 3, 4], 3, 4)
    [4, 3, 0, 1, 2]
    '''
    # Rotate so that current_position is at the front (N.B. This also copies
    # the list, which prevents mutating the original list.)
    lst = lst[current_position:] + lst[:current_position]
    # Reverse
    lst[:length] = lst[:length][::-1]
    # Rotate back
    lst = lst[-current_position:] + lst[:-current_position]
    return lst


def knot_hash(s):
    # Preprocessing
    lengths = [ord(ch) for ch in s] + [17, 31, 73, 47, 23]

    # 64 rounds of hashing
    current_position = 0
    skip_size = 0
    items = list(range(LIST_SIZE))
    for _ in range(64):
        for length in lengths:
            items = reverse(items, current_position, length)
            current_position = (current_position + length + skip_size) % LIST_SIZE
            skip_size += 1

    # Convert sparse hash to dense hash
    sparse_hash = items
    dense_hash = []
    for block_start in range(0, 256, 16):
        block = sparse_hash[block_start : block_start + 16]
        dense_hash.append(reduce(xor, block))

    # Convert dense hash to string
    result = ''
    for n in dense_hash:
        result += f'{n:02x}'
    return result


if __name__ == '__main__':
    main()
