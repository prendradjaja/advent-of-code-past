import collections as cl, sys
from util import findint


# TODO: Could be interesting to do this with an event loop instead of scanning
# possibly all `bot_storages` every time in `find_active_bot()`


BotRule = cl.namedtuple('BotRule', 'lo hi')
InputRule = cl.namedtuple('InputRule', 'value target')


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]

    # Parse
    bot_rules = {}
    input_rules = []
    for line in lines:
        if line.startswith('bot'):
            bid, rule = parse_bot_rule(line)
            bot_rules[bid] = rule
        elif line.startswith('value'):
            input_rules.append(parse_input_rule(line))

    # Provide inputs
    bot_storages = cl.defaultdict(list)
    for irule in input_rules:
        bot_storages[irule.target].append(irule.value)

    # Propagate chips
    while (bid := find_active_bot(bot_storages)) is not None:
        storage = bot_storages[bid]
        storage.sort()
        lo, hi = storage

        if storage == [17, 61]:
            print('Part 1 answer:')
            print(findint(bid))

        storage[:] = []
        brule = bot_rules[bid]
        bot_storages[brule.lo].append(lo)
        bot_storages[brule.hi].append(hi)

    # Examine outputs
    o0 ,= bot_storages['output 0']
    o1 ,= bot_storages['output 1']
    o2 ,= bot_storages['output 2']
    print()
    print('Part 2 answer:')
    print(o0 * o1 * o2)


def find_active_bot(bot_storages):
    for bid, storage in bot_storages.items():
        if len(storage) == 2 and bid.startswith('bot'):
            assert len(storage) == 2
            return bid
    return None


def parse_bot_rule(rulestr):
    '''
    >>> parse_bot_rule('bot 2 gives low to bot 1 and high to bot 0')
    ('bot 2', BotRule(lo='bot 1', hi='bot 0'))
    >>> parse_bot_rule('bot 1 gives low to output 1 and high to bot 0')
    ('bot 1', BotRule(lo='output 1', hi='bot 0'))
    '''
    bid, loname_and_hi_to_hiname = rulestr.split(' gives low to ')
    loname, hiname = loname_and_hi_to_hiname.split(' and high to ')
    return (bid, BotRule(loname, hiname))


def parse_input_rule(rulestr):
    '''
    >>> parse_input_rule('value 3 goes to bot 1')
    InputRule(value=3, target='bot 1')
    '''
    value_n, target = rulestr.split(' goes to ')
    return InputRule(findint(value_n), target)


if __name__ == '__main__':
    main()
