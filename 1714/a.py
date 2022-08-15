import sys
from day10 import knot_hash


MY_PUZZLE_INPUT = 'amgozmfv'


def main():
    puzzle_input = sys.argv[1] if len(sys.argv) > 1 else MY_PUZZLE_INPUT

    used = 0
    for row in range(128):
        hexstring = knot_hash(f'{puzzle_input}-{row}')
        number = int(hexstring, 16)
        bitstring = f'{number:0128b}'
        for bit in bitstring:
            if bit == '1':
                used += 1
    print(used)


if __name__ == '__main__':
    main()
