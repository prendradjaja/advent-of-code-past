import sys

def main():
    components = []
    for line in open(sys.argv[1]).read().splitlines():
        a, b = line.split('/')
        a = int(a)
        b = int(b)
        components.append(tuple(sorted((a, b))))
    components.sort()
    assert len(components) == len(set(components))

    get_all(components)
    # print(make_bridge(components, [0]))
    # print(make_bridge(components, [0, 0]))
    # print(make_bridge(components, [0, 0, 0]))
    # print(make_bridge(components, [1]))
    # print(make_bridge(components, [1, 0]))
    # print(make_bridge(components, [1, 0, 0]))
    # print(make_bridge(components, [1, 0, 0, 0]))
    # print(make_bridge(components, [1, 0, 0, 1]))
    # print(make_bridge(components, [1, 1]))
    # print(make_bridge(components, [1, 1, 0]))
    # print(make_bridge(components, [1, 1, 1]))

    # indices = []
    # while True:
    #     print()
    #     bridge = make_bridge(components, indices)
    #     print(bridge)
    #     for i, option in enumerate(options := get_options(components, bridge)):
    #         print(i, option)
    #     i = int(input())
    #     indices.append(i)

def get_all(components):
    indices = (0,)
    i = 0
    best = 0
    try:
        while True:
            i += 1
            best = max(best, strength(make_bridge(components, indices)))
            if i % 1000 == 0:
                print(i // 1000, '?', indices)
            # print(make_bridge(components, indices))
            if is_valid(components, deepen(indices)):
                indices = deepen(indices)
            elif is_valid(components, increment(indices)):
                indices = increment(indices)
            else:
                indices = carry_increment(indices)
                while not is_valid(components, indices):
                    indices = carry_increment(indices)
                    if indices == ():
                        return
    except IndexError:
        print(best)

def strength(bridge):
    return sum(a + b for (a, b) in bridge)

def is_valid(components, indices):
    try:
        make_bridge(components, indices)
        return True
    except IndexError:
        return False

def deepen(indices):
    return indices + (0,)

def increment(indices):
    '''
    >>> increment((0,))
    (1,)
    >>> increment((0, 0))
    (0, 1)
    >>> increment((0, 0, 0))
    (0, 0, 1)
    '''
    last = indices[-1]
    return indices[:-1] + (last+1,)

def carry_increment(indices):
    '''
    '''
    return increment(indices[:-1])

def make_bridge(components, indices):
    bridge = []
    for idx in indices:
        options = get_options(components, bridge)
        bridge.append(options[idx])
    return bridge

def get_options(components, bridge):
    pins = get_pins(bridge)
    unused = sorted(set(components) - set(bridge))
    return [c for c in unused if pins in c]

def get_pins(bridge):
    if not bridge:
        return 0
    else:
        pins = 0
        for component in bridge:
            pins = get_other_pins(component, pins)
        return pins

def get_other_pins(component, pins):
    if component[0] == pins:
        return component[1]
    else:
        return component[0]

if __name__ == '__main__':
    main()
