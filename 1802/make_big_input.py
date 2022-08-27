import random
from string import ascii_lowercase


def main():
    boxids = open('in').read().strip().splitlines()
    boxids.extend([random_box_id() for _ in range(100_000)])
    random.shuffle(boxids)
    for each in boxids:
        print(each)


def random_box_id():
    return ''.join(random.choice(ascii_lowercase) for _ in range(26))


main()
