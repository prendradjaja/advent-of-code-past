import sys
from util import transpose, findints

def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    total = 0
    for line in lines:
        if possible(*findints(line)):
            total += 1
    print(total)

def possible(a, b, c):
    if a + b <= c:
        return False
    if a + c <= b:
        return False
    if b + c <= a:
        return False
    return True

main()
