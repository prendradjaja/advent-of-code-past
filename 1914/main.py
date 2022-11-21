from collections import namedtuple, defaultdict
import math


ReactionDef = namedtuple('ReactionDef', 'left right')
QuantifiedChemical = namedtuple('QuantifiedChemical', 'quantity chemical')


def main():
    pass


def run_forwards(reactions, allowed_reactions):
    available = defaultdict(int)
    for step in reactions:
        result_chemical, multiplier = step
        reaction = allowed_reactions[result_chemical]

        for quantity, input_chemical in reaction.left:
            consumed = quantity * multiplier
            assert available[input_chemical] >= consumed or input_chemical == 'ORE'
            available[input_chemical] -= consumed

        available[result_chemical] += reaction.right.quantity * multiplier

    ore_consumed = -available['ORE']
    del available['ORE']

    return ore_consumed, dict(available)


def back_one_step(quantified_chemical, allowed_reactions):
    '''
    >>> allowed_reactions = parse("""
    ... 1 ORE => 10 A
    ... 1 A => 1 B
    ... 5 A, 5 B => 1 FUEL
    ... """)
    >>> back_one_step(QuantifiedChemical(10, 'A'), allowed_reactions)
    ([QuantifiedChemical(quantity=1, chemical='ORE')], [])
    >>> back_one_step(QuantifiedChemical(20, 'A'), allowed_reactions)
    ([QuantifiedChemical(quantity=2, chemical='ORE')], [])

    >>> back_one_step(QuantifiedChemical(1, 'A'), allowed_reactions)
    ([QuantifiedChemical(quantity=1, chemical='ORE')], [QuantifiedChemical(quantity=9, chemical='A')])
    >>> back_one_step(QuantifiedChemical(11, 'A'), allowed_reactions)
    ([QuantifiedChemical(quantity=2, chemical='ORE')], [QuantifiedChemical(quantity=9, chemical='A')])
    >>> back_one_step(QuantifiedChemical(21, 'A'), allowed_reactions)
    ([QuantifiedChemical(quantity=3, chemical='ORE')], [QuantifiedChemical(quantity=9, chemical='A')])
    '''
    desired_quantity, chemical = quantified_chemical
    reaction = allowed_reactions[chemical]

    multiplier = math.ceil(desired_quantity / reaction.right.quantity)
    needed = [mul(multiplier, qc) for qc in reaction.left]
    extra_quantity = multiplier * reaction.right.quantity - desired_quantity
    if extra_quantity:
        extra = [QuantifiedChemical(extra_quantity, chemical)]
    else:
        extra = []
    return (needed, extra)


def add(qcs1, qcs2):
    result = defaultdict(int)
    for each in qcs1 + qcs2:
        quantity, chemical = each
        result[chemical] += quantity
    return [QuantifiedChemical(quantity, chemical) for (chemical, quantity) in result.items()]


def show_one(quantified_chemical, *, print_=True):
    quantity, chemical = quantified_chemical
    result = f'{quantity} {chemical}'
    if print_:
        print(result)
    else:
        return result


def show_many(qcs):
    print(', '.join(show_one(qc, print_=False) for qc in qcs))


def mul(multiplier, quantified_chemical):
    return QuantifiedChemical(
        quantified_chemical.quantity * multiplier,
        quantified_chemical.chemical
    )


def parse(text):
    result = {}
    for line in text.strip().splitlines():
        left, right = line.split(' => ')
        left = [parse_quantified_chemical(each) for each in left.split(', ')]
        right = parse_quantified_chemical(right)
        result[right.chemical] = ReactionDef(left, right)
    return result


def parse_quantified_chemical(text):
    quantity, chemical = text.split(' ')
    return QuantifiedChemical(
        int(quantity),
        chemical
    )


if __name__ == '__main__':
    main()
