import sys
from util import findints, Record


VERBOSE = False

Firewall = Record('Firewall', 'depth range scanner_position movement_direction')


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    firewalls = []
    for line in lines:
        depth, my_range = findints(line)
        firewalls.append(Firewall(depth, my_range, 0, 1))

    last_depth = depth

    trip_severity = 0
    for picosecond in range(0, last_depth+1):
        # Advance the packet and check if caught
        if (
            (current_firewall := find(firewalls, lambda fw: fw.depth == picosecond))
            and current_firewall.scanner_position == 0
        ):
            layer_severity = current_firewall.depth * current_firewall.range
            trip_severity += layer_severity
            if VERBOSE:
                print(f'Caught at depth {current_firewall.depth}, range {current_firewall.range} for severity {layer_severity}')

        # Advance the scanners
        for firewall in firewalls:
            next_position = firewall.scanner_position + firewall.movement_direction
            if next_position in [-1, firewall.range]:
                firewall.movement_direction *= -1
                next_position = firewall.scanner_position + firewall.movement_direction
            firewall.scanner_position = next_position

    print(trip_severity)



def find(lst, pred):
    matches = [x for x in lst if pred(x)]
    if matches:
        return matches[0]
    else:
        return None


if __name__ == '__main__':
    main()
