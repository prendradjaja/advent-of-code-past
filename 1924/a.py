def main():
    text = open('in').read().strip()
    seen = {text}
    while True:
        text = step(text)
        if text in seen:
            break
        seen.add(text)
    print(biodiversity_rating(text))

def step(text):
    '''
    >>> text = """
    ... ....#
    ... #..#.
    ... #..##
    ... ..#..
    ... #....
    ... """.strip()

    >>> text = step(text)
    >>> print(text)
    #..#.
    ####.
    ###.#
    ##.##
    .##..

    >>> text = step(text)
    >>> print(text)
    #####
    ....#
    ....#
    ...#.
    #.###

    >>> text = step(text)
    >>> print(text)
    #....
    ####.
    ...##
    #.##.
    .##.#

    >>> text = step(text)
    >>> print(text)
    ####.
    ....#
    ##..#
    .....
    ##...
    '''
    grid = text.splitlines()
    result = ''
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            pos = (r, c)
            if ch == '#' and live_neighbors(grid, pos) != 1:
                result += '.'
            elif ch == '.' and live_neighbors(grid, pos) in [1, 2]:
                result += '#'
            else:
                result += ch
        result += '\n'
    return result.rstrip('\n')

def live_neighbors(grid, pos):
    result = 0
    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor_pos = addvec(pos, offset)
        if in_bounds(grid, neighbor_pos):
            result += getindex(grid, neighbor_pos) == '#'
    return result

def in_bounds(grid, pos):
    r, c = pos
    return (
        0 <= r < len(grid) and
        0 <= c < len(grid[0])
    )

def addvec(v, w):
    return (v[0] + w[0], v[1] + w[1])

def getindex(grid, pos):
    r, c = pos
    return grid[r][c]

def biodiversity_rating(text):
    '''
    >>> text = """
    ... .....
    ... .....
    ... .....
    ... #....
    ... .#...
    ... """.strip()
    >>> biodiversity_rating(text)
    2129920
    '''
    binary = (
        text
            .replace('\n', '')
            .replace('.', '0')
            .replace('#', '1')
            [::-1]
    )
    return int(binary, 2)

if __name__ == '__main__':
    main()
