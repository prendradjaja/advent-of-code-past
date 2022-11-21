'''
Greedy/naive approach -- this figures out *some* amount of ore that can be
consumed to produce a chemical, but since the approach doesn't keep track of
"extra" matter produced by each reaction, this amount is not guaranteed to be
minimal. In fact, for the first example given in the problem description, it
is not minimal! (Result is 41, but 31 can be achieved.)

I might throw this code away, but it might be useful!
'''

from main import *


def main():
    '''
    >>> main()
    1 FUEL
    7 A, 1 E
    10 ORE, 7 A, 1 D
    20 ORE, 7 A, 1 C
    30 ORE, 7 A, 1 B
    41 ORE
    '''
    allowed_reactions = parse('''
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
    ''')
    back_many_steps_naive(QuantifiedChemical(1, 'FUEL'), allowed_reactions)


def back_many_steps_naive(quantified_chemical, allowed_reactions):
    qcs = [quantified_chemical]

    while len(qcs) > 1 or qcs[0].chemical != 'ORE':
        show_many(qcs)
        qcs = expand(qcs, allowed_reactions)
    show_many(qcs)


def expand(qcs, allowed_reactions):
    qcss = [
        (
            back_one_step(qc, allowed_reactions)[0]
            if qc.chemical != 'ORE'
            else [qc]
        )
        for qc in qcs
    ]
    result = []
    for each in qcss:
        result = add(result, each)
    return result


if __name__ == '__main__':
    main()
