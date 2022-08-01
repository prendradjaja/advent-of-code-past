import sys
import string
from gridlib import gridsource as gridlib


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    grid = [l.rstrip('\n') for l in f]
    start_col = grid[0].index('|')

    position = (0, start_col)
    direction = (1, 0)
    letters = ''
    steps = 0
    while True:
        position = gridlib.addvec(position, direction)
        steps += 1

        value = gridlib.getindex(grid, position)
        if value == ' ':
            break
        elif value in '|-':
            pass
        elif value == '+':
            direction = find_turn_direction(grid, position, direction)
        elif value in string.ascii_uppercase:
            letters += value
        else:
            raise Exception('Unexpected value')

    print('Part 1 answer:', letters)
    print('Part 2 answer:', steps)


def find_turn_direction(grid, position, direction):
    backwards = gridlib.mulvec(direction, -1)
    all_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    all_other_directions = [d for d in all_directions if d != backwards]
    for offset in all_other_directions:
        neighbor_position = gridlib.addvec(position, offset)
        neighbor_value = gridlib.getindex(grid, neighbor_position)
        if neighbor_value != ' ':
            return offset
    raise Exception('Turn direction not found')


if __name__ == '__main__':
    main()
