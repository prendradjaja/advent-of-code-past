import sys
import collections
from util import consecutives


first_row = '.^.^..^......^^^^^...^^^...^...^....^^.^...^.^^^^....^...^^.^^^...^^^^.^^.^.^^..^.^^^..^^^^^^.^^^..^'
total_row_count = 400000

# # Example input 1
# first_row = '..^^.'
# total_row_count = 3

# # Example input 2
# first_row = '.^^.^.^^^^'
# total_row_count = 10


rules = collections.defaultdict(lambda: '.')
rules['^^.'] = '^'
rules['.^^'] = '^'
rules['^..'] = '^'
rules['..^'] = '^'


def main():
    new_row_count = total_row_count - 1
    row = first_row
    safe_count = len([tile for tile in row if tile == '.'])
    # print(row)
    for _ in range(new_row_count):
        row = step(row)
        # print(row)
        safe_count += len([tile for tile in row if tile == '.'])

    print('\nAnswer:')
    print(safe_count)


def step(row):
    padded = '.' + row + '.'
    result = ''
    for neighborhood in consecutives(padded, 3, string=True):
        result += rules[neighborhood]
    return result


if __name__ == '__main__':
    main()
