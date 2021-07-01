from collections import defaultdict


def main():
    target = 20
    plants, rules = read_and_parse()
    for _ in range(target):
        plants = iterate(plants, rules)
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


if __name__ == '__main__':
    main()
