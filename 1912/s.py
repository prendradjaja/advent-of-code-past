import fileinput, collections, collections as cl, itertools, itertools as it, math, random, sys, re, string, functools
from gridlib import gridsource as gridlib, gridcustom # *, gridsource, gridcardinal, gridplane
from util import *


Moon = Record('Moon', 'pos vel')


def main():
    # Config
    path = sys.argv[1] if len(sys.argv) > 1 else 'in'
    n = 1000 if path == 'in' else 100
    print('path:', path)
    print('n:', n)

    # Parse
    f = open(path)
    lines = [l.rstrip('\n') for l in f]
    moons = []
    for line in lines:
        pos = tuple(findints(line))
        moons.append(Moon(pos, (0, 0, 0)))

    # Simulate
    for _ in range(n):
        # Update velocities
        for a, b in itertools.combinations(moons, 2):
            diffs = gridlib.subvec(a.pos, b.pos)
            signs = tuple(sign(n) for n in diffs)
            a.vel = gridlib.subvec(a.vel, signs)
            b.vel = gridlib.addvec(b.vel, signs)

        # Update positions
        for moon in moons:
            moon.pos = gridlib.addvec(moon.pos, moon.vel)

    # Compute energy
    total = 0
    for moon in moons:
        pot = gridlib.absmanhattan(moon.pos)
        kin = gridlib.absmanhattan(moon.vel)
        total += pot * kin

    print('\nAnswer:')
    print(total)


def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0


if __name__ == '__main__':
    main()
