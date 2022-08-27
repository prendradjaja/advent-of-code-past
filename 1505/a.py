VOWELS = 'aeiou'
BANNED_STRINGS = ['ab', 'cd', 'pq', 'xy']


def main():
    answer = 0
    for line in open('in').read().strip().splitlines():
        answer += int(is_nice(line))
    print(answer)


def is_nice(s):
    '''
    >>> is_nice('ugknbfddgicrmopn')
    True
    >>> is_nice('aaa')
    True
    >>> is_nice('jchzalrnumimnmhp')
    False
    >>> is_nice('haegwjzuvuyypxyu')
    False
    >>> is_nice('dvszwmarrgswjxmb')
    False
    '''
    return (
        # At least three vowels
        len([ch for ch in s if ch in VOWELS]) >= 3

        # At least one double letter
        and any(a == b for (a, b) in zip(s, s[1:]))

        # Does not contain any of ab, cd, pq, xy
        and all(banned not in s for banned in BANNED_STRINGS)
    )


if __name__ == '__main__':
    main()
