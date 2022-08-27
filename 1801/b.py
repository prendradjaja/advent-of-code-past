import itertools

changes = [int(line) for line in open('in').read().strip().splitlines()]
freq = 0
seen = {freq}
for n in itertools.cycle(changes):
    freq += n
    if freq in seen:
        print(freq)
        break
    seen.add(freq)
