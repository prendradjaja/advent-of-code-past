'''
Usage:

# Run against my puzzle input
python3 b.py

# Run against your puzzle input
python3 b.py PATH_TO_PUZZLE_INPUT

# Show ASCII art visualization
python3 b.py ex -v
'''

import sys
import itertools
from util import findints, Record


Firewall = Record('Firewall', 'depth range scanner_position movement_direction')
Packet = Record('Packet', 'depth delay')


def main():
    '''
    Remarks:

    First (much too slow) approach was to simulate one packet moving through
    the firewall. Eventually the packet hits a scanner -- at that point, stop
    the simulation and start over. Repeat this for every possible delay value
    (0, 1, 2, 3, ...).

    This solution is just an optimization on top of that same idea: Instead of
    simulating one packet then restarting the simulation at every collision
    with a scanner, simulate a continuous stream of packets.

    There must be a better way to do this, but hey -- it works :)
    '''
    global input_lines
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'in'
    verbose = '-v' in sys.argv

    f = open(input_path)
    input_lines = [l.rstrip('\n') for l in f]

    firewalls = initialize_firewalls()
    packets = []

    finish_line = max(firewall.depth for firewall in firewalls) + 1

    while True:
        advance_scanners(firewalls)
        advance_packets_and_spawn(packets, firewalls, finish_line)
        if verbose:
            show(firewalls, packets)


def show(firewalls, packets):
    image = {}
    for firewall in firewalls:
        c = firewall.depth * 4
        for r in range(firewall.range):
            image[r,c] = '['
            image[r,c+2] = ']'
        r = firewall.scanner_position
        image[r,c+1] = 'S'
    for packet in packets:
        c = packet.depth * 4 + 1
        r = 0
        image[r,c] = '*'
    rmin = min(r for (r,c) in image)
    rmax = max(r for (r,c) in image)
    cmin = min(c for (r,c) in image)
    cmax = max(c for (r,c) in image)
    for r in range(rmin, rmax+1):
        for c in range(cmin, cmax+1):
            print(image.get((r,c), ' '), end='')
        print()
    print()


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


time = 0
def advance_packets_and_spawn(packets, firewalls, finish_line):
    '''
    Spawn a packet at the start, then advance all packets
    '''
    global time
    time += 1
    if time % 10000 == 0:
        print(f'... {time:,}')
    packets.append(Packet(-1, time))
    to_remove = []
    for p in packets:
        p.depth += 1
        if (
            # Check for collision
            (current_firewall := find(firewalls, lambda fw: fw.depth == p.depth))
            and current_firewall.scanner_position == 0
        ):
            to_remove.append(p)
        elif p.depth == finish_line:
            print('Answer:', p.delay)
            exit()
    for p in to_remove:
        packets.remove(p)


def find(lst, pred):
    matches = [x for x in lst if pred(x)]
    if matches:
        return matches[0]
    else:
        return None


if __name__ == '__main__':
    main()
