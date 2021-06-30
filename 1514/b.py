from collections import namedtuple
from util import *

class Reindeer:
    def __init__(self, speed, run_duration, rest_duration):
        self.speed = speed
        self.run_duration = run_duration
        self.rest_duration = rest_duration

        self.mode = 'run'
        self.second = 0
        self.position = 0

        self.points = 0

    def tick(self):
        if self.mode == 'run':
            self.position += self.speed
            self.second += 1
            if self.second == self.run_duration:
                self.second = 0
                self.mode = 'rest'
        else:
            self.second += 1
            if self.second == self.rest_duration:
                self.second = 0
                self.mode = 'run'

def multimax(lst, key=lambda x: x):
    '''
    >>> multimax([1, 2, 3])
    [3]
    >>> multimax([1, 2, 3, 3])
    [3, 3]
    >>> multimax([1, 2, 3], key=lambda x: -x)
    [1]
    >>> multimax([1, 1, 2, 3], key=lambda x: -x)
    [1, 1]
    '''
    return [x for x in lst if key(x) == key(max(lst, key=key))]

if __name__ == '__main__':
    reindeer = [Reindeer(*findints(line)) for line in open('input.txt')]

    for _ in range(2503):
        for r in reindeer:
            r.tick()
        for r in multimax(reindeer, key=lambda r: r.position):
            r.points += 1

    print(max(r.points for r in reindeer))
