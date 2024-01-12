from sscanf import sscanf
from collections import namedtuple
import sys

from gridlib import gridcardinal as gridlib


# TODO Rename SAND, CLAY to EMPTY, WALL to avoid bugs
SAND = '.'
CLAY = '#'
SPRING = '+'

SPRING_POS = (500, 0)

FLOWING_WATER = '|'
RESTING_WATER = '~'

SOLID = [CLAY, RESTING_WATER]

DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():

    solve()

    # demo()


def solve():
    world = World.from_scan(open(sys.argv[1]).read(), SPRING_POS)
    from fixtures import PLATFORM, CUP_R, TWO_STREAMS, NARROW_TUB_BUG
    import time
    import os

    def animate(n, sleep):
        os.system('clear')
        world.show()
        time.sleep(sleep)
        for _ in range(n):
            world.step()
            os.system('clear')
            world.show()
            time.sleep(sleep)

    # world = World.from_ascii_art(NARROW_TUB_BUG)
    animate(500, 0.01)
    print(world.count_water())
    return

    i = 0
    prev_water = None
    while True:
        if i % 1000 == 0:
            water = world.count_water()
            print(i // 1000, water)
            if water == prev_water:
                break
            prev_water = water

        world.step()
        i += 1


def demo():
    from fixtures import PLATFORM, CUP_R, TWO_STREAMS, NARROW_TUB_BUG
    import time
    import os

    def animate(n, sleep):
        os.system('clear')
        world.show()
        time.sleep(sleep)
        for _ in range(n):
            world.step()
            os.system('clear')
            world.show()
            time.sleep(sleep)

    world = World.from_ascii_art(NARROW_TUB_BUG)
    animate(100, 0.01)


class World:
    def __init__(self, clay, springs):
        self.clay = clay
        self.springs = springs
        self.flowing_water = set()
        self.resting_water = set()
        self.max_y = max(y for (x, y) in self.clay)

        # Simulate first step -- this isn't done in step() because it's an edge
        # case that's implemented differently
        for pos in self.springs:
            below_spring = gridlib.addvec(pos, DOWN)
            assert self.is_empty(below_spring)
            self.flowing_water.add(below_spring)

    def is_empty(self, pos):
        return (
            pos not in self.clay and
            pos not in self.springs and
            pos not in self.flowing_water and
            pos not in self.resting_water
        )

    @classmethod
    def from_ascii_art(cls, ascii_art):
        clay = set()
        springs = set()
        for y, line in enumerate(ascii_art.splitlines()):
            for x, ch in enumerate(line):
                pos = x, y
                if ch == '.':
                    pass
                elif ch == CLAY:
                    assert pos not in springs
                    clay.add(pos)
                elif ch == SPRING:
                    assert pos not in clay
                    springs.add(pos)
                else:
                    raise Exception(f'unexpected character: {ch}')
        return cls(clay, springs)

    @classmethod
    def from_scan(cls, text, spring_pos):
        clay = set()
        springs = [spring_pos]
        for line in text.splitlines():
            axis_a, a, _, b1, b2 = (
                line
                .replace('=', ' ')
                .replace(',', ' ')
                .replace('.', ' ')
                .split()
            )
            a = int(a)
            b1 = int(b1)
            b2 = int(b2)
            # axis_a, a, _, b1, b2 = sscanf(line, '%s=%u, %s=%u..%u')
            assert b2 > b1
            for b in range(b1, b2+1):
                if axis_a == 'x':
                    pos = (a, b)
                else:
                    assert axis_a == 'y'
                    pos = (b, a)
                clay.add(pos)
        return cls(clay, springs)

    def get(self, pos):
        assert 1 >= (
            (pos in self.clay) +
            (pos in self.springs) +
            (pos in self.flowing_water) +
            (pos in self.resting_water)
        )
        if pos in self.clay:
            return CLAY
        elif pos in self.springs:
            return SPRING
        elif pos in self.flowing_water:
            return FLOWING_WATER
        elif pos in self.resting_water:
            return RESTING_WATER
        else:
            return SAND

    def show(self):
        # Could just use `for (x, y) in self.clay`, but would have to update unit tests
        spring = self.springs[0]
        min_x = spring[0] - 80
        max_x = spring[0] + 10
        min_y = spring[1] - 20
        max_y = spring[1] + 20
        padding = 3
        for y in range(min_y - padding, max_y + padding + 1):
            for x in range(min_x - padding, max_x + padding + 1):
                pos = (x, y)
                ch = self.get(pos)
                print(ch, end='')
            print()
        print()

    def count_water(self):
        return len(self.flowing_water) + len(self.resting_water)

    def step(self):
        frontier = self._find_frontier()
        self._propagate_frontier(frontier)
        self._narrow_tub_hack()

    def _propagation_destinations(self, pos):
        down = gridlib.addvec(pos, DOWN)
        left = gridlib.addvec(pos, LEFT)
        right = gridlib.addvec(pos, RIGHT)
        down_value = self.get(down)
        left_value = self.get(left)
        right_value = self.get(right)

        if (
            down_value == SAND
        ):
            if down[1] <= self.max_y:
                return [down]
            else:
                return []
        elif (
            down_value in SOLID
            and (left_value == SAND or right_value == SAND)
        ):
            result = []
            if left_value == SAND:
                result.append(left)
            if right_value == SAND:
                result.append(right)
            return result
        else:
            return []

    def _find_frontier(self):
        result = []
        for pos in self.flowing_water:
            if self._propagation_destinations(pos):
                result.append(pos)
        return result

    def _propagate_frontier(self, frontier):
        for pos in frontier:
            for new_pos in self._propagation_destinations(pos):
                assert self.is_empty(new_pos)
                self.flowing_water.add(new_pos)
                self._maybe_become_resting_water(new_pos)

    def _narrow_tub_hack(self):
        to_rest = []
        for pos in self.flowing_water:
            down = self.get(gridlib.addvec(pos, DOWN))
            left = self.get(gridlib.addvec(pos, LEFT))
            right = self.get(gridlib.addvec(pos, RIGHT))
            if (
                down in SOLID and
                left == CLAY and
                right == CLAY
            ):
                to_rest.append(pos)
        for pos in to_rest:
            self._rest_one_water_cell(pos)

    def _maybe_become_resting_water(self, pos):
        assert pos in self.flowing_water
        left_edge = pos
        right_edge = pos
        while self.get(gridlib.addvec(left_edge, LEFT)) == FLOWING_WATER:
            left_edge = gridlib.addvec(left_edge, LEFT)
        while self.get(gridlib.addvec(right_edge, RIGHT)) == FLOWING_WATER:
            right_edge = gridlib.addvec(right_edge, RIGHT)


        pos = left_edge
        cells = []
        while pos != gridlib.addvec(right_edge, RIGHT):
            cells.append(pos)
            pos = gridlib.addvec(pos, RIGHT)

        everything_below_is_solid = all(
            self.get(gridlib.addvec(pos, DOWN)) in SOLID for pos in cells
        )

        if (
            self.get(gridlib.addvec(left_edge, LEFT)) == CLAY and
            self.get(gridlib.addvec(right_edge, RIGHT)) == CLAY and
            everything_below_is_solid
        ):
            for pos in cells:
                self._rest_one_water_cell(pos)
                # TODO this line below can be removed
                pos = gridlib.addvec(pos, RIGHT)

    def _rest_one_water_cell(self, pos):
        assert pos in self.flowing_water
        self.flowing_water.remove(pos)
        self.resting_water.add(pos)



if __name__ == '__main__':
    main()
