import hashlib
import sys
import itertools


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    text = f.read().strip()
    password = {}
    for n in itertools.count():
        my_hash = md5(f'{text}{n}')
        if (
            my_hash.startswith('00000')
            and my_hash[5] not in password
            and '0' <= my_hash[5] < '8'
        ):
            password[my_hash[5]] = my_hash[6]
            print(n, my_hash, password)
        if len(password) == 8:
            break
    print(''.join(v for k, v in sorted(password.items())))


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    main()
