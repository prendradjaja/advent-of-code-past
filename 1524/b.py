import sys
import itertools
import math


def main():
    text = open(sys.argv[1] if len(sys.argv) > 1 else 'in').read()
    packages = [int(n) for n in text.strip().splitlines()]

    assert sum(packages) % 4 == 0
    desired_weight = sum(packages) // 4

    group_size = find_first_group_size(packages, desired_weight)
    answer = min(
        math.prod(group)
        for group in itertools.combinations(packages, group_size)
        if sum(group) == desired_weight
    )
    print(answer)



def find_first_group_size(packages, desired_weight):
    for group_size in range(2, len(packages)):
        for group in itertools.combinations(packages, group_size):
            if sum(group) == desired_weight:
                return group_size


if __name__ == '__main__':
    main()
