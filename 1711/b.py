import sys
from gridlib import gridsource as gridlib


DIRECTIONS = {
    'n': (-2, 0),
    'ne': (-1, 1),
    'se': (1, 1),
    's': (2, 0),
    'sw': (1, -1),
    'nw': (-1, -1),
}


def main():
    text = open(sys.argv[1] if len(sys.argv) > 1 else 'in').read().strip()
    commands = text.split(',')

    position = (0, 0)
    max_distance = 0
    for each in commands:
        position = gridlib.addvec(position, DIRECTIONS[each])
        max_distance = max(
            max_distance,
            distance_from_origin(position)
        )
    print(max_distance)


def distance_from_origin(position):
    # Explanation:
    #
    # Points along the south axis or southeast axis are easy. Other points can
    # be divided into three cases / regions, which are a bit trickier.
    #
    # (Of course, there are nine more regions if you allow negative coordinates,
    # but these can be reduced to the cases we've already described by taking
    # the absolute values of the coordinates.)
    #
    # To find the distance for a point in region A, count northwestward steps
    # until you reach the south axis (see diagram), then count northward
    # steps until you reach the origin.
    #
    # Regions B and C are similar:
    # - Region B: count northward steps until the southeast axis, then count
    #   northwestward steps until the origin
    # - Region C: count southwestward steps until the southeast axis, then count
    #   northwestward steps until the origin
    #
    # And that's it!
    #
    #
    #     Origin
    #     *-_- - -*- - - -*- - - -*- - - -*- - - -*- - - -*  Halfway between southeast and northeast (a.k.a. east)
    #     |\  * _     *       *       *       *       *
    #    (#)\     * _     *       *       *       *       *
    #     |  \*       * _     *       *       *       *
    #    (#)   \  *       * _     *       *      (C)      *
    #     |   * \     *       * _     *       *       *
    #    (#)     \*       *       * _     *       *       *
    #     |   *    \  *       *       * _     *       *
    #    (#)      * \     *       *       * _     *       *
    #     |   *      \*       *       *       * _     *
    #    (#)      *    \  *      (B)      *       * _     *
    #     |   *       * \     *       *       *       * _
    #    (#)      *      \*       *       *       *       *  Southeast axis
    #     |   *       *    \  *       *       *       *
    #    (#)      *       * \     *       *       *
    #     |  (#)      *      \*       *       *
    #     *      (A)      *    \  *       *
    #     |   *       *       * \     *
    #     *       *       *      \* Halfway between south and southeast
    #     |   *       *       *
    #     *       *       *
    #     |   *       *
    #     *       *
    #     |   *
    #     *
    #     South axis

    r, c = position
    r = abs(r)
    c = abs(c)
    if c == 0:  # Easy case: Point is on the south axis
        return r // 2
    elif r == c:  # Easy case: Point is on the southeast axis
        return r
    elif r > c:
        distance_from_south_axis = c
        distance_from_southeast_axis = (r - c) // 2
        if distance_from_south_axis < distance_from_southeast_axis:  # Region A case
            c = 0
            r = r - distance_from_south_axis
            return distance_from_south_axis + distance_from_origin( (r, c) )
        else:  # Region B case
            r = c
            return distance_from_southeast_axis + distance_from_origin( (r, c) )
    elif r < c:  # Region C case
        distance_from_southeast_axis = 0
        while r != c:
            r, c = gridlib.addvec( (r, c), DIRECTIONS['sw'] )
            distance_from_southeast_axis += 1
        return distance_from_southeast_axis + distance_from_origin( (r, c) )


# Alternatively, a concise solution adapted from <https://www.redblobgames.com/grids/hexagons/#distances-doubled>

# def distance_from_origin(position):
#     r, c = position
#     r = abs(r)
#     c = abs(c)
#     return c + max(0, (r - c) // 2)


if __name__ == '__main__':
    main()
