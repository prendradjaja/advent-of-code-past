import itertools
from util import *

def look_and_say(n = '1'):
    while True:
        yield n
        next_item = ''
        for digit, items in itertools.groupby(str(n)):
            count = str(ilen_exhaustive(items))
            next_item += count + digit
        n = next_item

sequence = look_and_say('3113322113')
for _ in range(50):
    next(sequence)

print(len(next(sequence)))
