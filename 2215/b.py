from dataclasses import dataclass
from collections import namedtuple

from sscanf import sscanf


Point = namedtuple('Point', 'x y')


def main():
    INPUT_PATH = 'in'
    SEARCH_AREA_MIN = 0
    SEARCH_AREA_MAX = 4000000

    sensors = []
    beacons = set()
    for line in open(INPUT_PATH).read().splitlines():
        sx, sy, bx, by = sscanf(line, 'Sensor at x=%s, y=%s: closest beacon is at x=%s, y=%s')
        sx = int(sx)
        sy = int(sy)
        bx = int(bx)
        by = int(by)
        beacon = Point(bx, by)
        beacons.add(beacon)
        sensor = Sensor(
            Point(sx, sy),
            beacon
        )
        sensors.append(sensor)

    print('Searching... (This will take some time)')
    progress_interval = SEARCH_AREA_MAX // 20
    for y in range(0, SEARCH_AREA_MAX + 1):
        if y % progress_interval == 0:
            progress = round(100 * y / SEARCH_AREA_MAX)
            print(f'... {progress}%')

        iset = IntervalSet()
        for sensor in sensors:
            my_slice = sensor.get_slice(y)
            if my_slice:
                iset.add(my_slice)

        if (
            len(iset.intervals) == 1
            and iset.intervals[0].lo <= SEARCH_AREA_MIN
            and iset.intervals[0].hi >= SEARCH_AREA_MAX
        ):
            pass  # Distress beacon is not at this y value
        else:
            assert len(iset.intervals) == 2
            i1, i2 = iset.intervals
            assert i1.hi + 2 == i2.lo

            x = i1.hi + 1
            answer = x * 4000000 + y

            print('\nAnswer:')
            print(answer)
            print('\nFinishing search... (To prove there is only one possible position)')

    print('\nDone. The answer should have been printed above.')


def manhattan_distance(p1, p2):
    dx = abs(p1.x - p2.x)
    dy = abs(p1.y - p2.y)
    return dx + dy


@dataclass(frozen=True)
class Sensor:
    position: Point
    closest_beacon: Point

    def get_radius(self):
        return manhattan_distance(self.position, self.closest_beacon)

    def get_slice(self, slice_y):
        '''
        Returns an Interval or None (if slice_y is too far away for there to be a slice)
        '''
        delta_y = abs(self.position.y - slice_y)
        slice_radius = self.get_radius() - delta_y
        if slice_radius < 0:
            return None
        else:
            return Interval(
                self.position.x - slice_radius,
                self.position.x + slice_radius
            )


class IntervalSet:
    def __init__(self):
        self.intervals = []

    def add(self, new_interval):
        intervals2 = []
        for interval in self.intervals:
            combine_result = interval.combine(new_interval)
            is_combined = combine_result[0]
            if not is_combined:
                intervals2.append(interval)
            else:
                new_interval = combine_result[1]
        intervals2.append(new_interval)
        intervals2.sort(key = lambda x: x.lo)
        self.intervals = intervals2

    def contains(self, x):
        return any(interval.contains(x) for interval in self.intervals)

    def size(self):
        return sum(interval.size() for interval in self.intervals)


@dataclass(frozen=True)
class Interval:
    '''
    A closed interval (i.e. endpoints are included)
    '''
    lo: int
    hi: int

    def __str__(self):
        return f'[{self.lo}, {self.hi}]'

    def __post_init__(self):
        assert self.hi >= self.lo

    def size(self):
        return self.hi - self.lo + 1

    def contains(self, x):
        return self.lo <= x <= self.hi

    def to_set(self):
        return set(range(self.lo, self.hi + 1))

    def combine(self, other):
        '''
        Returns either

        (True, combined_interval, None)
        # If combineable

        or

        (False, self, other)
        # If not combineable
        '''
        if self.lo >= other.hi + 2:
            return (False, self, other)
        elif other.lo >= self.hi + 2:
            return (False, self, other)
        else:
            combined_interval = Interval(
                min(self.lo, other.lo),
                max(self.hi, other.hi),
            )
            return (True, combined_interval, None)


if __name__ == '__main__':
    main()
