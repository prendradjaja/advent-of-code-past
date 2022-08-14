import sys
from gridlib import gridsource as gridlib


# I think the coordinate system I used is the "doubled coordinates" system
# described here: <https://www.redblobgames.com/grids/hexagons/>
DIRECTIONS = {
    'n': (-2, 0),
    'ne': (-1, 1),
    'se': (1, 1),
    's': (2, 0),
    'sw': (1, -1),
    'nw': (-1, -1),
}


def main():
    text = open(sys.argv[1] if len(sys.argv) > 1 else 'in').read().strip()
    commands = text.split(',')

    position = (0, 0)
    for each in commands:
        position = gridlib.addvec(position, DIRECTIONS[each])
    print('Final position:', position)

    northeasts = 437
    norths = 387
    assert (0, 0) == gridlib.addvec(
        gridlib.addvec(
            position,
            gridlib.mulvec(DIRECTIONS['ne'], northeasts)
        ),
        gridlib.mulvec(DIRECTIONS['n'], norths)
    )
    print('Answer:', northeasts + norths)


if __name__ == '__main__':
    main()
