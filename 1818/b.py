'''
It would take too long to simulate 1000000000 steps! But we don't have to.

As it turns out, after several hundred days, the simulation begins to repeat
the same states over and over again in a fixed cycle.

Run b_appendix.py (or open table.txt) to see a table of simulation results.
Here are some portions of the table, with commentary:

n       first   val
0       -       289962   <-- The initial state of the land has a Total
1       -       348650       Resource Value of ~289k (rounded down).
2       -       425448
3       -       511648

8       -       589935
9       -       513238
10      -       427961   <-- After 10 days, the land has a TRV of ~427k.

464     -       76874
465     -       77315
466     431     77822    <-- After 466 days, we start to see repetition. The
467     432     80948        431 in the second column indicates that the
468     433     85910        arrangement of acres after 466 days is identical
469     434     90155        to after 431 days -- the second column is "On what
470     435     95232        day was this arrangement of acres first seen?"

499     464     76874
500     465     77315
501     431     77822    <-- The cycle starts over again!
502     432     80948
503     433     85910

This cycle of 35 days repeats forever. Using the values from this table, we
can extrapolate to 1000000000 days without simulating 1000000000 steps.
'''

known_values = {
    431: 77822,
    432: 80948,
    433: 85910,

    434: 90155, 435: 95232, 436: 97782, 437: 101840, 438: 105183, 439: 103880,
    440: 103970, 441: 101802, 442: 97350, 443: 94579, 444: 89436, 445: 91581,
    446: 87250, 447: 88893, 448: 92232, 449: 96012, 450: 98814, 451: 100466,
    452: 101840, 453: 103224, 454: 102366, 455: 97270, 456: 92839, 457: 91425,
    458: 88894, 459: 86320, 460: 82984, 461: 81788, 462: 78324,

    463: 77361,
    464: 76874,
    465: 77315,
}

period = len(known_values)  # -> 35

modulo_table = {
    key % period: value
    for key, value in known_values.items()
}

def extrapolate(n):
    '''
    >>> extrapolate(466)
    77822
    >>> extrapolate(500)
    77315
    '''
    assert n > max(known_values)
    return modulo_table[n % period]

print(extrapolate(1000000000))
