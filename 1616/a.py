def main():
    puzzle_input = '11100010111110100'
    disk_size = 272

    print(solve(puzzle_input, disk_size))

def solve(puzzle_input, disk_size):
    text = puzzle_input

    while len(text) < disk_size:
        text = dragon_step(text)

    text = text[:disk_size]
    return checksum(text)


def dragon_step(a):
    b = ''.join(reversed(a))
    b = invert(b)
    return a + '0' + b


def invert(s):
    result = ''
    for ch in s:
        assert ch in '01'
        other = '1' if ch == '0' else '0'
        result += other
    return result


def checksum(text):
    assert len(text) % 2 == 0
    result = ''
    for i in range(0, len(text), 2):
        pair = text[i : i+2]
        left, right = pair
        result += str(int(bool(left == right)))  # '0' or '1'
    if len(result) % 2 == 1:
        return result
    else:
        return checksum(result)


if __name__ == '__main__':
    main()
