import sys
import math
from gridlib import gridsource as gridlib
from util import findints


def main():
    global ingredients

    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    ingredients = []
    for line in lines:
        ingredients.append(
            tuple(findints(line))[:-1]  # Last item is calories: Remove it
        )

    answer = max(score(amounts) for amounts in get_amounts())
    print(answer)


def score(amounts):
    totals = (0,) * len(ingredients[0])
    for amount, ingredient in zip(amounts, ingredients):
        totals = gridlib.addvec(
            totals,
            gridlib.mulvec(ingredient, amount)
        )
    if any(value <= 0 for value in totals):
        return 0
    else:
        return math.prod(totals)


def get_amounts():
    '''
    Generator that yields all possible ways of splitting 100 into four parts.

    >>> amounts = get_amounts()
    >>> next(amounts)
    (0, 0, 0, 100)
    >>> next(amounts)
    (0, 0, 1, 99)

    And so on...
    '''

    total = 100
    remainder = total - 0
    for a in range(0, remainder+1):
        remainder = total - (a)
        for b in range(0, remainder+1):
            remainder = total - (a + b)
            for c in range(0, remainder+1):
                remainder = total - (a + b + c)
                d = remainder
                assert a + b + c + d == total
                yield a, b, c, d


if __name__ == '__main__':
    main()
