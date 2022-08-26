import re


WIDTH = 50
HEIGHT = 6


def main():
    global grid
    grid = [[' '] * WIDTH for _ in range(HEIGHT)]

    # Run instructions
    for line in open('in').read().splitlines():
        if line.startswith('rect '):
            a, b = ints(re.fullmatch(r'rect (\d+)x(\d+)', line).groups())
            rect(a, b)
        elif line.startswith('rotate column '):
            x, amount = ints(re.fullmatch(r'rotate column x=(\d+) by (\d+)', line).groups())
            rotate_column(x, amount)
        elif line.startswith('rotate row '):
            y, amount = ints(re.fullmatch(r'rotate row y=(\d+) by (\d+)', line).groups())
            rotate_row(y, amount)
        else:
            assert False

    answer = 0
    for row in grid:
        for value in row:
            if value == '#':
                answer += 1
    print('Part 1 answer:', answer)

    print('Part 2 answer:')
    for row in grid:
        print(''.join(row))


def ints(strings):
    return [int(n) for n in strings]


def rect(a, b):
    for x in range(a):
        for y in range(b):
            grid[y][x] = '#'


def rotate_list(lst, amount):
    '''
    >>> rotate_list([1, 2, 3, 4, 5], 2)
    [4, 5, 1, 2, 3]
    >>> rotate_list([1, 2, 3, 4, 5], 0)
    [1, 2, 3, 4, 5]
    >>> rotate_list([1, 2, 3, 4, 5], 5)
    [1, 2, 3, 4, 5]
    '''
    return lst[-amount:] + lst[:-amount]


def rotate_column(x, amount):
    column = [grid[y][x] for y in range(HEIGHT)]
    column = rotate_list(column, amount)
    for y in range(HEIGHT):
        grid[y][x] = column[y]


def rotate_row(y, amount):
    row = grid[y]
    row[:] = rotate_list(row, amount)


# # Alternative implementation
# def rotate_row(y, amount):
#     row = [grid[y][x] for x in range(WIDTH)]
#     row = rotate_list(row, amount)
#     for x in range(WIDTH):
#         grid[y][x] = row[x]


main()
