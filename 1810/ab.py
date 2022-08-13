import sys
from types import SimpleNamespace as obj

from gridlib import gridsource as gridlib
from util import findints, Record


Star = Record('Star', 'position velocity')


def main():
    # Parse
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    stars = []
    for line in lines:
        px, py, vx, vy = findints(line)
        star = Star((px, py), (vx, vy))
        stars.append(star)


    # Simulate and look for a local minimum of get_width()
    prev_width = float('inf')
    steps = 0
    while True:
        for star in stars:
            star.position = gridlib.addvec(star.position, star.velocity)

        width = get_width(stars)
        if width > prev_width:
            break
        prev_width = width

        steps += 1


    # Undo last step
    for star in stars:
        star.position = gridlib.subvec(star.position, star.velocity)


    # Print answers
    print('Part 1 answer:\n')
    extent = get_extent(stars)
    for y in range(extent.ymin, extent.ymax + 1):
        for x in range(extent.xmin, extent.xmax + 1):
            if any(s.position == (x, y) for s in stars):
                print('#', end='')
            else:
                print('.', end='')
        print()

    print('\nPart 2 answer:')
    print(steps)


def get_width(stars):
    extent = get_extent(stars)
    return extent.xmax - extent.xmin


def get_extent(stars):
    return obj(
        xmin = min(s.position[0] for s in stars),
        xmax = max(s.position[0] for s in stars),
        ymin = min(s.position[1] for s in stars),
        ymax = max(s.position[1] for s in stars),
    )


if __name__ == '__main__':
    main()
