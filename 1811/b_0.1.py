PUZZLE_INPUT = 5535


def main():
    grid = make_grid(PUZZLE_INPUT, 300)
    best_value = float('-inf')
    best_subgrid = None
    for subgrid_size in range(1, 300 + 1):
        print('...', subgrid_size)
        for x in range(1, 300 - subgrid_size + 2):
            for y in range(1, 300 - subgrid_size + 2):
                corner = (x, y)
                value = get_subgrid_sum(grid, corner, subgrid_size)
                if value > best_value:
                    best_value = value
                    best_subgrid = (*corner, subgrid_size)
    print(','.join(str(x) for x in best_subgrid))


def get_subgrid_sum(grid, corner, size):
    '''
    Find the sum of the subgrid of GRID of the given SIZE and top-left CORNER.
    '''
    key = (id(grid), corner, size)
    smallerkey = (id(grid), corner, size - 1)

    if size == 1:
        result = grid[corner]
    else:
        if smallerkey not in get_subgrid_sum.cache:
            get_subgrid_sum(grid, corner, size - 1)

        assert smallerkey in get_subgrid_sum.cache

        margin_sum = 0
        x0, y0 = corner

        x = x0 + size - 1
        for y in range(y0, y0 + size - 1):  # -1 to avoid double-counting the corner
            margin_sum += grid[(x, y)]

        y = y0 + size - 1
        for x in range(x0, x0 + size):
            margin_sum += grid[(x, y)]

        result = get_subgrid_sum.cache[smallerkey] + margin_sum

    get_subgrid_sum.cache[key] = result
    return result
get_subgrid_sum.cache = {}


def make_grid(serialno, size):
    grid = {}
    for x in range(1, size+1):
        for y in range(1, size+1):
            # Find the fuel cell's rack ID, which is its X coordinate plus 10.
            rid = x + 10

            # Begin with a power level of the rack ID times the Y coordinate.
            power = rid * y

            # Increase the power level by the value of the grid serial number
            # (your puzzle input).
            power += serialno

            # Set the power level to itself multiplied by the rack ID.
            power *= rid

            # Keep only the hundreds digit of the power level (so 12345
            # becomes 3; numbers with no hundreds digit become 0).
            power = (power // 100) % 10

            # Subtract 5 from the power level.
            power -= 5

            grid[(x, y)] = power

    return grid


main()
