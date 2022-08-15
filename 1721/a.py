import sys
import collections
import math
from util import enumerate2d, rotmat, fliphorz


Square = collections.namedtuple('Square', 'flat pos')


INITIAL_IMAGE = '''
.#.
..#
###
'''.strip().splitlines()


def main():
    # Parse input file and build rules dict (including rotations and reflections)
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = f.read().splitlines()
    rules = {}
    for line in lines:
        left, right = line.split(' => ')
        for newleft in rotations_and_reflections(left):
            rules[newleft] = right

    # Enhance the image
    image = INITIAL_IMAGE
    for _ in range(5):
        image = enhance(image, rules)

    # Count pixels
    count_on = 0
    for _, pixel in enumerate2d(image):
        if pixel == '#':
            count_on += 1
    print(count_on)


def enhance(image, rules):
    squares = to_squares(image)

    if get_square_size(image) == 2:
        scale1d = lambda coord: coord * 3 // 2
    else:
        scale1d = lambda coord: coord * 4 // 3
    scale2d = lambda pos: (scale1d(pos[0]), scale1d(pos[1]))

    new_squares = [
        Square(
            rules[square.flat],
            scale2d(square.pos)
        )
        for square in squares
    ]

    return from_squares(new_squares)


def rotations_and_reflections(flat_square):
    image = from_squares([Square(flat_square, (0, 0))])
    image = [list(row) for row in image]
    result = []
    for _ in range(4):
        result.append(to_squares(image)[0].flat)
        result.append(to_squares(fliphorz(image))[0].flat)
        image = rotmat(image)
    return result


def to_squares(image):
    image_size = len(image)
    square_size = get_square_size(image)

    squares = []
    # For each square
    for r in range(0, image_size, square_size):
        for c in range(0, image_size, square_size):
            flat = ''
            # For each pixel in the square
            for i in range(square_size):
                for j in range(square_size):
                    flat += image[r+i][c+j]
                flat += '/'
            flat = flat.rstrip('/')
            square = Square(flat, (r, c))
            squares.append(square)

    return tuple(squares)


def from_squares(squares):
    square_size = len(squares[0].flat.split('/')[0])

    image_size_in_squares = math.isqrt(len(squares))
    assert image_size_in_squares * image_size_in_squares == len(squares)
    image_size = image_size_in_squares * square_size

    image = [[None] * image_size for _ in range(image_size)]

    for square in squares:
        for i in range(square_size):
            for j in range(square_size):
                pixel = square.flat[i * (square_size + 1) + j]
                image[square.pos[0] + i][square.pos[1] + j] = pixel

    for _, pixel in enumerate2d(image):
        assert pixel is not None

    image = [''.join(row) for row in image]
    return image


def get_square_size(image):
    image_size = len(image)
    if image_size % 2 == 0:
        return 2
    else:
        assert image_size % 3 == 0
        return 3


if __name__ == '__main__':
    main()
