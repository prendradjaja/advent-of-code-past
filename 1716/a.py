import sys
from util import ints
from string import ascii_lowercase


def main():
    # f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')

    f = open('in')
    programs = list(ascii_lowercase[:16])

    # f = open('ex')
    # programs = list(ascii_lowercase[:5])

    dance = f.read().split(',')

    for move in dance:
        move = move.strip()
        if move[0] == 's':
            n = int(move[1:])
            programs = programs[-n:] + programs[:-n]
        elif move[0] == 'x':
            left, right = ints(move[1:].split('/'))
            programs[left], programs[right] = programs[right], programs[left]
        elif move[0] == 'p':
            left, right = move[1:].split('/')
            i = programs.index(left)
            j = programs.index(right)
            programs[i], programs[j] = programs[j], programs[i]
        else:
            1/0

    print(''.join(programs))


if __name__ == '__main__':
    main()
