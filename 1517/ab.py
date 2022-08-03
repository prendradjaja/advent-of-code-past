import itertools


# Example input
desired_total = 25
containers = [20, 15, 10, 5, 5]

# Puzzle input
desired_total = 150
containers = [33, 14, 18, 20, 45, 35, 16, 35, 1, 13, 18, 13, 50, 44, 48, 6, 24, 41, 30, 42]


def power_set(items):
    count_items = len(items)
    for i in range(2 ** count_items):
        bits = bin(i)[2:].zfill(count_items)
        yield tuple(items[j] for j in range(count_items) if bits[j] == '1')


combinations = [subset for subset in power_set(containers) if sum(subset) == desired_total]
combinations.sort(key=len)

print('Part 1 answer:', len(combinations))

for n, combinations_of_length_n in itertools.groupby(combinations, len):
    break

print('Part 2 answer:', len(list(combinations_of_length_n)))
