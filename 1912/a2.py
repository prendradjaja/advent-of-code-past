from util import Record, transpose

import re
import itertools
import sys


Moon1D = Record('Moon1D', 'pos vel')


def main():
    # Parse
    lines = open(sys.argv[1]).read().splitlines()
    lines = [
        re.sub(r'[^-0-9]', ' ', line)
            .strip()
            .split()
        for line in lines
    ]
    moon_positions = [[int(n) for n in line] for line in lines]

    # Split into "parallel universes":
    #
    # Since physics in each dimension is independent (e.g. physics in the X
    # dimension doesn't affect physics in the Y dimension), we can pretend
    # there are three one-dimensional universes (X, Y, Z), which each contain
    # a copy of each moon. Each universe can be simulated separately.
    #
    # This trick is not actually needed for Part 1, but it's key for Part 2.
    universes = transpose(moon_positions)
    universes = [[Moon1D(pos, 0) for pos in universe] for universe in universes]

    # Simulate
    for _ in range(1000):
        for universe in universes:
            step(universe)

    # Calculate total energy
    moons = list(zip(*universes))
    total_energy = sum(total_energy_of_moon(moon) for moon in moons)
    print(total_energy)


def check_cycle_length(universe):
    initial_state = freeze(universe)
    for i in itertools.count(1):
        step(universe)
        if freeze(universe) == initial_state:
            return i


def step(universe):
    # Apply gravity
    for a, b in itertools.combinations(universe, 2):
        if a.pos > b.pos:
            a.vel -= 1
            b.vel += 1
        elif a.pos < b.pos:
            a.vel += 1
            b.vel -= 1

    # Apply velocities
    for moon in universe:
        moon.pos += moon.vel


def total_energy_of_moon(moon):
    potential_energy = sum(
        abs(dimension.pos)
        for dimension in moon
    )
    kinetic_energy = sum(
        abs(dimension.vel)
        for dimension in moon
    )
    return potential_energy * kinetic_energy


def freeze(universe):
    return str(universe)


if __name__ == '__main__':
    main()
