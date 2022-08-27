import re
from collections import Counter
from string import ascii_lowercase


def main():
    answer = 0
    for line in open('in').read().strip().splitlines():
        name, sector_id, checksum = parse(line)
        if checksum == get_checksum(name):
            print(decrypt(name, sector_id), sector_id)

    print('\nTo find the answer, manually look (or e.g. grep, CTRL-F, etc) through this')
    print('output for a sector name that looks like it would store North Pole objects.')


def parse(fullname):
    PATTERN = (
        r'([-a-z]+)' +
        r'-' +
        r'([0-9]+)' +
        r'\[([a-z]+)\]'
    )
    name, sector_id, checksum = re.fullmatch(PATTERN, fullname).groups()
    return name, int(sector_id), checksum


def get_checksum(name):
    _ = name                                       # e.g. 'aaaa-cc-bb-defg
    _ = [ch for ch in _ if ch != '-']              # e.g. 'aaaaccbbdefg
    _ = Counter(_).most_common()                   # e.g. [('a', 4), ('c', 2), ('b', 2), ('d', 1), ('e', 1), ('f', 1), ('g', 1)]
    _ = [(y, x) for (x, y) in _]                   # e.g. [(4, 'a'), (2, 'c'), (2, 'b'), (1, 'd'), (1, 'e'), (1, 'f'), (1, 'g')]
    _.sort(key=lambda tpl: (-tpl[0], tpl[1]))      # e.g. [(4, 'a'), (2, 'b'), (2, 'c'), (1, 'd'), (1, 'e'), (1, 'f'), (1, 'g')]
    _ = ''.join(ch for (count, ch) in _)           # e.g. 'abcdef...'
    _ = _[:5]                                      # e.g. 'abcde'
    return _


def decrypt(name, sector_id):
    result = ''
    for ch in name:
        if ch in ascii_lowercase:
            idx = ascii_lowercase.index(ch)
            idx = (idx + sector_id) % len(ascii_lowercase)
            result += ascii_lowercase[idx]
        else:
            result += ch
    return result


if __name__ == '__main__':
    main()
