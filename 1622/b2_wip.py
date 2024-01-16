#!/usr/bin/env python3
'''
Usage:
    ./b2.py PATH_TO_INPUT_FILE
'''

import sys


def main():
    world = [list(line) for line in open(sys.argv[1]).read().splitlines()]
    for each in world:
        print(' '.join(each))


if __name__ == '__main__':
    main()
