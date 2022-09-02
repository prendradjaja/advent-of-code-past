WIDTH = 25
HEIGHT = 6


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

    layer = min(layers, key=lambda l: count(l, '0'))
    answer = count(layer, '1') * count(layer, '2')
    print(answer)


def count(layer, digit):
    result = 0
    for row in layer:
        for ch in row:
            if ch == digit:
                result += 1
    return result


if __name__ == '__main__':
    main()
