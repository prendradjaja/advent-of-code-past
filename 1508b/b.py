import sys


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    answer = 0
    for line in lines:
        len_original = len(line)
        len_encoded = len(line) + 2 + len([x for x in line if x in '"\\"'])
        answer += len_encoded - len_original
    print(answer)


if __name__ == '__main__':
    main()
