from collections import defaultdict
import itertools
from util import *

def main():
    # people[A][B] = X means person A would gain X points by sitting next to B
    people = defaultdict(lambda: defaultdict(int))
    for line in open('input.txt'):
        line = line.replace(' lose ', ' gain -')
        name, *_, neighbor = line.split()
        neighbor = neighbor.replace('.', '')
        points = findint(line)
        people[name][neighbor] = points

    # Add me to the seating chart. Since this is a defaultdict, getting = adding
    people['me']

    best_arrangement = max(itertools.permutations(people), key=lambda perm: score(perm, people))
    print(score(best_arrangement, people))


def score(arrangement, people):
    total = 0
    for a, b in consecutives(list(arrangement) + [arrangement[0]]):
        total += people[a][b]
        total += people[b][a]
    return total


if __name__ == '__main__':
    main()
