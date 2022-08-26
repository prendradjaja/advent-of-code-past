import hashlib
import itertools


def main():
    puzzle_input = 'ckczppom'
    zeroes = '0' * 5
    for n in itertools.count(1):
        if md5(f'{puzzle_input}{n}').startswith(zeroes):
            print(n)
            break


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


main()
