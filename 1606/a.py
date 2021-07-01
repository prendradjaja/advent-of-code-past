import collections as cl, sys

def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]

    # counts[pos][ch] = how many times character `ch` appeared in position `pos`
    counts = cl.defaultdict(cl.Counter)
    for line in lines:
        for i, c in enumerate(line):
            counts[i][c] += 1

    for pos in sorted(counts):
        print(max(counts[pos],
                  key=lambda ch: counts[pos][ch]),
              end='')

main()
