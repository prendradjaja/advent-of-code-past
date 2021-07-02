import collections as cl, sys
from util import transpose

def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]

    columns = transpose(lines)
    for col in columns:
        print(cl.Counter(col).most_common()[-1][0], end='')
    print()


main()
