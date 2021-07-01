import itertools
from collections import defaultdict


def main():
    target = 50_000_000_000

    plants, rules = read_and_parse()
    for g in itertools.count():
        next_plants = iterate(plants, rules)
        is_offset, offset = check_offset(plants, next_plants)
        if is_offset:
            break

        plants = next_plants

    # At this point, `plants` is the state after g generations.

    assert offset == 1

    # From this point on, every plant moves to the right one pot per g.

    plants = {p + target - g for p in plants}
    print(sum(plants))


def read_and_parse():
    puzzle_input = open('input.txt')

    plants = set()
    for i, ch in enumerate(next(puzzle_input).strip().split()[-1]):
        if ch == '#':
            plants.add(i)

    next(puzzle_input)  # discard blank line

    rules = {}
    for line in puzzle_input:
        line = line.strip()
        left, right = line.split(' => ')
        rules[left] = right

    return plants, rules


def iterate(plants, rules):
    new_plants = set()

    for i in range(min(plants)-2, max(plants)+3):
        neighborhood = ''.join('.#'[j in plants] for j in range(i-2, i+3))
        if rules[neighborhood] == '#':
            new_plants.add(i)

    return new_plants


def check_offset(plants1, plants2):
    '''
    Returns (boolean, number) of:

    [0]: Are plants2 and plants1 "the same but offset"?
    [1]: If yes, what is the offset? (If no: None)
    '''
    # "relative locations" of plants
    rel1 = {p - min(plants1) for p in plants1}
    rel2 = {p - min(plants2) for p in plants2}

    if rel1 != rel2:
        return (False, None)

    return (True, min(plants2) - min(plants1))


if __name__ == '__main__':
    main()
