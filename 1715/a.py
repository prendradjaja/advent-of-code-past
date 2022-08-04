def main():
    # # Example input
    # initial_values = 65, 8921

    # Puzzle input
    initial_values = 289, 629

    a0, b0 = initial_values

    a = make_generator(a0, 16807)
    b = make_generator(b0, 48271)

    matches = 0
    for _ in range(40_000_000):
        matches += int(
            low16(next(a)) == low16(next(b))
        )
    print(matches)


def low16(n):
    return bin(n)[2:][-16:].zfill(16)



def make_generator(initial_value, factor):
    n = initial_value
    while True:
        n = (n * factor) % 2147483647
        yield n


if __name__ == '__main__':
    main()
