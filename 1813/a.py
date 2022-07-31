from gridlib import gridsource as gridlib
import sys
from collections import deque


DIRECTIONS = [
    DOWN := (1, 0),
    RIGHT := (0, 1),
    UP := (-1, 0),
    LEFT := (0, -1),
]

CART_SYMBOLS = 'v>^<'

SYMBOL_TO_DIRECTION = {
    'v': DOWN,
    '>': RIGHT,
    '^': UP,
    '<': LEFT,
}

DIRECTION_TO_SYMBOL = {
    DOWN: 'v',
    RIGHT: '>',
    UP: '^',
    LEFT: '<',
}

ANTICLOCKWISE = 1
STRAIGHT = 0
CLOCKWISE = -1


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    track = []
    carts = []
    for r, raw_line in enumerate(lines):
        track_line = (
            raw_line
                .replace('^', '|')
                .replace('v', '|')
                .replace('>', '-')
                .replace('<', '-')
        )
        track.append(track_line)
        for c, char in enumerate(raw_line):
            if char in CART_SYMBOLS:
                cart = Cart(char, (r, c), track)
                carts.append(cart)

    while True:
        tick(track, carts)


def tick(track, carts):
    '''
    Mutates items in carts (not carts itself)
    '''
    carts = sorted(carts, key=lambda cart: cart.position)
    for cart in carts:
        cart.move()
        other_carts = [c for c in carts if c is not cart]
        for other in other_carts:
            if cart.position == other.position:
                print(cart.get_xy_position())
                exit()


def show(track, carts):
    for r, track_line in enumerate(track):
        output_line = ''
        for c, track_char in enumerate(track_line):
            cart = find(carts, lambda cart: cart.position == (r, c))
            if cart:
                output_line += colored(cart.symbol(), 'red')
            else:
                output_line += track_char
        print(output_line)


def find(lst, pred):
    matches = [x for x in lst if pred(x)]
    if matches:
        return matches[0]
    else:
        return None


class Cart:
    def __init__(self, symbol, position, track):
        assert symbol in CART_SYMBOLS
        self.direction = SYMBOL_TO_DIRECTION[symbol]
        self.position = position
        self.turn_queue = deque([ANTICLOCKWISE, 0, CLOCKWISE])
        self.track = track

    def symbol(self):
        return DIRECTION_TO_SYMBOL[self.direction]

    def move(self):
        self.position = gridlib.addvec(self.position, self.direction)
        track_piece = gridlib.getindex(self.track, self.position)
        if track_piece == '\\':
            self.direction = {
                RIGHT: DOWN,
                DOWN: RIGHT,
                LEFT: UP,
                UP: LEFT,
            }[self.direction]
        elif track_piece == '/':
            self.direction = {
                RIGHT: UP,
                UP: RIGHT,
                LEFT: DOWN,
                DOWN: LEFT,
            }[self.direction]
        elif track_piece == '+':
            rotation = self.turn_queue.popleft()
            self.turn_queue.append(rotation)
            self.direction = turn(self.direction, rotation)

    def get_xy_position(self):
        return f'{self.position[1]},{self.position[0]}'


def turn(direction, rotation):
    '''
    >>> turn(UP, ANTICLOCKWISE) == LEFT
    True
    >>> turn(UP, CLOCKWISE) == RIGHT
    True
    >>> turn(UP, STRAIGHT) == UP
    True

    Edge cases: Wrapping around the beginning/end of DIRECTIONS
    >>> turn(LEFT, ANTICLOCKWISE) == DOWN
    True
    >>> turn(DOWN, CLOCKWISE) == LEFT
    True
    '''
    return DIRECTIONS[(DIRECTIONS.index(direction) + rotation) % 4]



if __name__ == '__main__':
    main()
