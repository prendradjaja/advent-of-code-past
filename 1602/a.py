KEYPAD = ('123', '456', '789')
DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


def main():
    pos = [1, 1]
    for line in open('in').read().strip().splitlines():
        for ch in line:
            addvecmut(pos, DIRECTIONS[ch])
            pos[0] = clamp(pos[0], 0, 2)
            pos[1] = clamp(pos[1], 0, 2)
        print(KEYPAD[pos[0]][pos[1]], end='')
    print()


def addvecmut(v, w):
    v[0] += w[0]
    v[1] += w[1]


def clamp(x, lo, hi):
    if x > hi:
        return hi
    elif x < lo:
        return lo
    else:
        return x


if __name__ == '__main__':
    main()
