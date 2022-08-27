from collections import defaultdict
import itertools


def main():
    answer = 0
    for line in open('in').read().strip().splitlines():
        answer += int(is_nice(line))
    print(answer)


def is_nice(s):
    '''
    >>> is_nice('qjhvhtzxzqqjkmpb')
    True
    >>> is_nice('xxyxx')
    True
    >>> is_nice('uurcxstgmygtbstg')
    False
    >>> is_nice('ieodomkazucvgmuy')
    False
    '''
    return has_double_pair(s) and has_xyx(s)


def has_double_pair(s):
    digraph_indices = defaultdict(list)
    for i in range(len(s) - 1):
        digraph = s[i : i+2]
        digraph_indices[digraph].append(i)

    for digraph, indices in digraph_indices.items():
        for i, j in itertools.combinations(indices, 2):
            if abs(i - j) != 1:
                return True
    return False


def has_xyx(s):
    return any(a == c for (a, b, c) in zip(s, s[1:], s[2:]))


if __name__ == '__main__':
    main()
