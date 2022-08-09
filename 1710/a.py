# list_size = 5
# lengths = [3, 4, 1, 5]

list_size = 256
lengths = [183,0,31,146,254,240,223,150,2,206,161,1,255,232,199,88]


def main():
    current_position = 0
    skip_size = 0
    items = list(range(list_size))

    for length in lengths:
        items = reverse(items, current_position, length)

        current_position += length + skip_size
        current_position %= list_size

        skip_size += 1

    answer = items[0] * items[1]
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


if __name__ == '__main__':
    main()
