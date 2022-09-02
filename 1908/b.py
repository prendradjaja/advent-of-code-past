WIDTH = 25
HEIGHT = 6

BLACK = '0'
WHITE = '1'
TRANSPARENT = '2'


def main():
    text = open('in').read().strip()

    DEPTH = len(text) // (WIDTH * HEIGHT)
    assert len(text) == WIDTH * HEIGHT * DEPTH

    layers = []
    for z in range(DEPTH):
        LAYER_SIZE = WIDTH * HEIGHT
        layertext = text[LAYER_SIZE * z : LAYER_SIZE * (z+1)]
        layer = []
        layers.append(layer)
        for r in range(HEIGHT):
            layer.append(layertext[WIDTH * r : WIDTH * (r+1)])

    image = {}
    for layer in layers[::-1]:
        for r, row in enumerate(layer):
            for c, ch in enumerate(row):
                pos = (r, c)
                if ch == BLACK:
                    image[pos] = '.'
                elif ch == WHITE:
                    image[pos] = '#'

    for r in range(HEIGHT):
        for c in range(WIDTH):
            ch = image.get((r, c), ' ')
            print(ch, end='')
        print()


if __name__ == '__main__':
    main()
