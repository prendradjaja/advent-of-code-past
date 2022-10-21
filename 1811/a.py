PUZZLE_INPUT = 5535


def main():
    grid = make_grid(PUZZLE_INPUT, 300)
    # corners = [
    #     (x, y)
    #     for x in range(1, 299)
    #     for y in range(1, 299)
    # ]
    # answer = max(
    #     corners,
    #     key=lambda corner: get_subgrid_sum(grid, corner, 3)
    # )
    # print(answer)

    print(get_subgrid_sum(grid, (19, 41), 3))


def get_subgrid_sum(grid, corner, size):
    '''
    Find the sum of the subgrid of GRID of the given SIZE and top-left CORNER.
    '''
    x0, y0 = corner
    return sum(
        grid[(x, y)]
        for x in range(x0, x0 + size)
        for y in range(y0, y0 + size)
    )


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
