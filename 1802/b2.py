'''
This solution's runtime is linear in the number of box ids (b.py's is
quadratic).

Try running it on big-input: It will finish relatively quickly, but b.py will
take a very long time.
'''


import sys


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'in'
    boxids = open(path).read().strip().splitlines()
    signature = search(boxids)
    answer = signature.replace('_', '')
    print(answer)


def search(boxids):
    seen = set()
    for boxid in boxids:
        for signature in signatures(boxid):
            if signature in seen:
                return signature
            seen.add(signature)


def signatures(s):
    '''
    >>> list(signatures('abcd'))
    ['_bcd', 'a_cd', 'ab_d', 'abc_']
    '''
    for i in range(len(s)):
        yield s[:i] + '_' + s[i+1:]


main()
