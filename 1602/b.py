KEYPAD = '''
#######
###1###
##234##
#56789#
##ABC##
###D###
#######
'''.strip().splitlines()
DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


def main():
    pos = (3, 3)
    for line in open('in').read().strip().splitlines():
        for ch in line:
            nextpos = addvec(pos, DIRECTIONS[ch])
            if getindex(KEYPAD, nextpos) != '#':
                pos = nextpos
        print(getindex(KEYPAD, pos), end='')
    print()


def addvec(v, w):
    return (v[0] + w[0], v[1] + w[1])


def getindex(grid, pos):
    r, c = pos
    return grid[r][c]


if __name__ == '__main__':
    main()
