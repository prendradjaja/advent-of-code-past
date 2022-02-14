import sys


def main():
    puzzle_input = '11100010111110100'
    part_1_disk_size = 272
    part_2_disk_size = 35651584

    print('Part 1 answer:', solve(puzzle_input, part_1_disk_size))

    print('\nPart 2:')
    part_2_answer = solve(puzzle_input, part_2_disk_size, verbose=True)
    print('Part 2 answer:', part_2_answer)

def solve(puzzle_input, disk_size, /, verbose=False):
    text = puzzle_input

    while len(text) < disk_size:
        text = dragon_step(text)
        if verbose:
            print(f'  Creating dragon. Length: {len(text):,}')
    if verbose:
        print('  Done creating dragon.')

    text = text[:disk_size]
    return checksum(text, verbose)


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


def checksum(text, /, verbose=False):
    if verbose:
        print(f'  Computing checksum. Length: {len(text):,}')
    assert len(text) % 2 == 0
    result = ''
    for i in range(0, len(text), 2):
        pair = text[i : i+2]
        left, right = pair
        result += str(int(bool(left == right)))  # '0' or '1'
    if len(result) % 2 == 1:
        return result
    else:
        return checksum(result, verbose=verbose)


if __name__ == '__main__':
    main()
