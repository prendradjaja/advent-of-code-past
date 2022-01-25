import hashlib
import sys
import itertools


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    text = f.read().strip()
    password = ''
    for n in itertools.count():
        my_hash = md5(f'{text}{n}')
        if my_hash.startswith('00000'):
            password += my_hash[5]
            print(n, my_hash, password)
        if len(password) == 8:
            break
    print(password)


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    main()
