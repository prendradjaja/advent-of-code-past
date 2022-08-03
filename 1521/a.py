import sys
import collections
import itertools as it
from util import findint


Fighter = collections.namedtuple('Fighter', 'max_hp damage armor')
Item = collections.namedtuple('Item', 'cost damage armor')


weapon_shop = {
    'Dagger':     Item(  8, 4, 0),
    'Shortsword': Item( 10, 5, 0),
    'Warhammer':  Item( 25, 6, 0),
    'Longsword':  Item( 40, 7, 0),
    'Greataxe':   Item( 74, 8, 0),
}

armor_shop = {
    'Leather':    Item( 13, 0, 1),
    'Chainmail':  Item( 31, 0, 2),
    'Splintmail': Item( 53, 0, 3),
    'Bandedmail': Item( 75, 0, 4),
    'Platemail':  Item(102, 0, 5),
}

ring_shop = {
    'Damage +1':  Item( 25, 1, 0),
    'Damage +2':  Item( 50, 2, 0),
    'Damage +3':  Item(100, 3, 0),
    'Defense +1': Item( 20, 0, 1),
    'Defense +2': Item( 40, 0, 2),
    'Defense +3': Item( 80, 0, 3),
}

shop = {
    **weapon_shop,
    **armor_shop,
    **ring_shop,
}


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    assert 'Hit Points' in lines[0]
    assert 'Damage' in lines[1]
    assert 'Armor' in lines[2]

    boss = Fighter(
        findint(lines[0]),
        findint(lines[1]),
        findint(lines[2])
    )

    min_winning_cost = float('inf')

    for weapon, armors, rings in it.product(
        # You must buy exactly one weapon; no dual-wielding.
        weapon_shop,
        # Armor is optional, but you can't use more than one.
        [(), *it.combinations(armor_shop, 1)],
        # You can buy 0-2 rings (at most one for each hand).
        [(), *it.combinations(ring_shop, 1), *it.combinations(ring_shop, 2)],
    ):
        items = [weapon, *armors, *rings]

        damage     = sum(shop[item].damage for item in items)
        armor      = sum(shop[item].armor  for item in items)
        total_cost = sum(shop[item].cost   for item in items)

        player = Fighter(100, damage, armor)

        if is_player_win(player, boss):
            min_winning_cost = min(min_winning_cost, total_cost)

    print(min_winning_cost)


def is_player_win(player, boss):
    player_hp = player.max_hp
    boss_hp = boss.max_hp
    while True:
        # Player attacks
        boss_hp -= max(player.damage - boss.armor, 1)
        if boss_hp <= 0:
            return True

        # Boss attacks
        player_hp -= max(boss.damage - player.armor, 1)
        if player_hp <= 0:
            return False


if __name__ == '__main__':
    main()
