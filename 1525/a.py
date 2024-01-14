#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
    ./b.py PATH_TO_INPUT_FILE
'''

import sys
import re


FIRST_CODE = 20151125
MULTIPLIER = 252533
DIVISOR = 33554393


def main():
    text = open(sys.argv[1]).read()
    row, col = [int(n) for n in re.findall(r'\d+', text)]

    n = get_grid_index(row, col)

    answer = FIRST_CODE * pow(MULTIPLIER, n - 1, DIVISOR) % DIVISOR
    print(answer)


def get_grid_index(r, c):
    '''
    Corresponds to this diagram
       | 1   2   3   4   5   6
    ---+---+---+---+---+---+---+
     1 |  1   3   6  10  15  21
     2 |  2   5   9  14  20
     3 |  4   8  13  19
     4 |  7  12  18
     5 | 11  17
     6 | 16

    >>> get_grid_index(3, 2)
    8
    '''
    diagonal_index = r + (c - 1)

    # The starts of each diagonal (1, 2, 4, 7, 11, 16, ...) form a quadratic
    # sequence (we know this because the lengths of each diagonal form an
    # arithmetc sequence), which we can easily find a closed-form expression
    # for:
    diagonal_start = diagonal_index**2//2 - diagonal_index//2 + 1

    return diagonal_start + (c - 1)

    # Or as one expression:
    # return (c**2 + 2*c*r - c + r**2 - 3*r + 2) // 2


if __name__ == '__main__':
    main()
