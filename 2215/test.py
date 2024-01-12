import random
import itertools
from collections import Counter

from b import Interval, IntervalSet


def main():

    # test_combine()

    # show_combine_examples()

    # test_add()

    # show_add_examples()

    pass


def show_add_examples():
    iset = IntervalSet()
    for _ in range(4):
        interval = get_random_interval()
        print(interval)
        iset.add(interval)
        print(iset.intervals)
        print()


def test_add():
    results = Counter()

    print(1)
    for lo1, hi1 in itertools.combinations(range(10), 2):
        interval1 = Interval(lo1, hi1)
        result = test_add_once([interval1])
        results[result] += 1

    print(2)
    for lo1, hi1 in itertools.combinations(range(10), 2):
        for lo2, hi2 in itertools.combinations(range(10), 2):
            interval1 = Interval(lo1, hi1)
            interval2 = Interval(lo2, hi2)
            result = test_add_once([interval1, interval2])
            results[result] += 1

    print(3)
    for lo1, hi1 in itertools.combinations(range(10), 2):
        for lo2, hi2 in itertools.combinations(range(10), 2):
            for lo3, hi3 in itertools.combinations(range(10), 2):
                interval1 = Interval(lo1, hi1)
                interval2 = Interval(lo2, hi2)
                interval3 = Interval(lo3, hi3)
                result = test_add_once([interval1, interval2, interval3])
                results[result] += 1

    print(4)
    for lo1, hi1 in itertools.combinations(range(8), 2):
        for lo2, hi2 in itertools.combinations(range(8), 2):
            for lo3, hi3 in itertools.combinations(range(8), 2):
                for lo4, hi4 in itertools.combinations(range(8), 2):
                    interval1 = Interval(lo1, hi1)
                    interval2 = Interval(lo2, hi2)
                    interval3 = Interval(lo3, hi3)
                    interval4 = Interval(lo4, hi4)
                    result = test_add_once([interval1, interval2, interval3, interval4])
                    results[result] += 1

    print(5)

    for key in results:
        print(key, results[key])


def test_add_once(intervals):
    # Get expected result
    expected = set()
    for interval in intervals:
        expected |= interval.to_set()

    # Get actual result
    iset = IntervalSet()
    for interval in intervals:
        iset.add(interval)
    actual = set()
    for interval in iset.intervals:
        actual |= interval.to_set()

    status = 'pass' if actual == expected else 'fail'
    return f'{status}, {len(intervals)} -> {len(iset.intervals)}'


def get_random_interval():
    a1 = random.choice(list(range(10)))
    b1 = random.choice(list(range(10)))
    interval1 = Interval(*sorted([a1, b1]))

    return interval1


def show_combine_examples():
    for _ in range(10):
        interval1 = get_random_interval()
        interval2 = get_random_interval()

        print(interval1, interval2, interval1.combine(interval2))


def test_combine():
    results = Counter()
    for lo1, hi1 in itertools.combinations_with_replacement(range(10), 2):
        for lo2, hi2 in itertools.combinations_with_replacement(range(10), 2):
            result = test_combine_once(lo1, hi1, lo2, hi2)
            results[result] += 1
    print(results)


def test_combine_once(lo1, hi1, lo2, hi2):
    interval1 = Interval(lo1, hi1)
    interval2 = Interval(lo2, hi2)

    expected = interval1.to_set() | interval2.to_set()

    combine_result = interval1.combine(interval2)
    is_combined = combine_result[0]

    if is_combined:
        actual = combine_result[1].to_set()
        if actual == expected:
            return 'pass combine case'
        else:
            return 'fail combine case'
    else:
        assert interval1 == combine_result[1]
        assert interval2 == combine_result[2]
        return 'non-combine case'


if __name__ == '__main__':
    main()
