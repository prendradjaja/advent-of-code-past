import itertools
import math


answer = 0
for line in open('in').read().strip().splitlines():
    row = [int(n) for n in line.split()]
    for a, b in itertools.combinations(row, 2):
        if math.gcd(a, b) in [a, b]:
            break
    a, b = sorted([a, b])
    answer += b // a
print(answer)
