'''
This almost certainly is the wrong approach. Chinese Remainder Theorem I
guess?

If this IS a workable approach, there probably is a way to take this from
quadratic(?) runtime to linear(?) -- don't start the simulation (scanner
positions) from scratch for every possible delay, but just do one simulation
with many packets.
'''

import sys
import itertools
from util import findints, Record


VERBOSE = True

Firewall = Record('Firewall', 'depth range scanner_position movement_direction')


def main():
    global input_lines
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    input_lines = [l.rstrip('\n') for l in f]

    for delay in itertools.count():
        caught = simulate(delay)
        if not caught:
            print('Answer:')
            print(delay)
            break
        if delay % 100 == 0:
            print(f'... {delay:,}')


def simulate(delay):
    '''
    Return True iff caught
    '''

    firewalls = initialize_firewalls()

    for _ in range(delay):
        advance_scanners(firewalls)

    max_depth = max(firewall.depth for firewall in firewalls)

    for picosecond in range(0, max_depth+1):
        # Advance the packet and check if caught
        if (
            (current_firewall := find(firewalls, lambda fw: fw.depth == picosecond))
            and current_firewall.scanner_position == 0
        ):
            return True

        # Advance the scanners
        advance_scanners(firewalls)

    return False


def initialize_firewalls():
    firewalls = []
    for line in input_lines:
        depth, my_range = findints(line)
        firewalls.append(Firewall(depth, my_range, 0, 1))
    return firewalls


def advance_scanners(firewalls):
    for firewall in firewalls:
        next_position = firewall.scanner_position + firewall.movement_direction
        if next_position in [-1, firewall.range]:
            firewall.movement_direction *= -1
            next_position = firewall.scanner_position + firewall.movement_direction
        firewall.scanner_position = next_position



def find(lst, pred):
    matches = [x for x in lst if pred(x)]
    if matches:
        return matches[0]
    else:
        return None


if __name__ == '__main__':
    main()
