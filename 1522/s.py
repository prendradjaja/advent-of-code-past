import fileinput, collections, collections as cl, itertools, itertools as it, math, random, sys, re, string, functools
from collections import namedtuple
from gridlib import gridsource as gridlib, gridcustom # *, gridsource, gridcardinal, gridplane
from util import *


Fighter = Record('Fighter', 'hp damage armor mana')
Effect = Record('Effect', 'name timer')

MAGIC_MISSILE = 'Magic Missile'
DRAIN = 'Drain'
SHIELD = 'Shield'
POISON = 'Poison'
RECHARGE = 'Recharge'

SPELLS = [MAGIC_MISSILE, DRAIN, SHIELD, POISON, RECHARGE]

SPELL_COSTS = {
    MAGIC_MISSILE: 53,
    DRAIN: 73,
    SHIELD: 113,
    POISON: 173,
    RECHARGE: 229,
}
assert list(SPELL_COSTS) == SPELLS

SPELL_DURATIONS = {
    MAGIC_MISSILE: None,
    DRAIN: None,
    SHIELD: 6,
    POISON: 6,
    RECHARGE: 5,
}
assert list(SPELL_DURATIONS) == SPELLS


# turn phases:
# - show stats
# - handle effects
# - check gameover
# - attack/spell
# - check gameover


def main():
    global boss, player
    global active_effects

    active_effects = []

    _ = 0

    # Example 1
    boss = Fighter(13, 8, _, _)
    player = Fighter(10, _, _, 250)

    # # Puzzle input
    # boss = Fighter(55, 8, _, _)  # TODO add kwargs support to Record constructor
    # player = Fighter(50, _, _, 500)

    player_turn(POISON)
    boss_turn()
    player_turn(MAGIC_MISSILE)
    boss_turn()


def player_turn(spell):
    assert spell in SPELLS

    log('-- Player turn --')
    log_stats()
    handle_effects()
    check_gameover()
    cast_spell(spell)
    check_gameover()
    log()


def boss_turn():
    log('-- Boss turn --')
    log_stats()
    handle_effects()
    check_gameover()
    boss_attack()
    check_gameover()
    log()


def handle_effects():
    to_remove = []
    for effect in active_effects:
        expired = handle_effect(effect)
        if expired:
            to_remove.append(effect)

    for effect in to_remove:
        active_effects.remove(effect)


def handle_effect(effect):
    '''
    Returns True if (and only if) the effect has now worn off.
    '''
    effect.timer -= 1

    if effect.name == SHIELD:
        pass  # TODO
    elif effect.name == POISON:
        damage = 3
        boss.hp -= damage
        log(f'{effect.name} deals {damage} damage; its timer is now {effect.timer}.')
    elif effect.name == RECHARGE:
        pass  # TODO
    else:
        1/0

    if effect.timer <= 0:
        log(f'{effect.name} wears off.')
        return True
    else:
        return False


def boss_attack():
    if player.armor:
        damage = max(boss.damage - player.armor, 1)
        log(f'Boss attacks for {boss.damage} - {player.armor} = {damage} damage!')
    else:
        damage = boss.damage
        log(f'Boss attacks for {damage} damage!')
    player.hp -= damage


def cast_spell(spell):
    assert spell in SPELLS

    spell_cost = SPELL_COSTS[spell]
    assert player.mana >= spell_cost, 'TODO handle this case?'
    player.mana -= spell_cost

    if spell == MAGIC_MISSILE:
        damage = 4
        boss.hp -= damage
        log(f'Player casts {spell}, dealing {damage} damage.')
        pass  # TODO
    elif spell == DRAIN:
        pass  # TODO
    elif spell == SHIELD:
        pass  # TODO
    elif spell == POISON:
        active_effects.append(Effect(spell, SPELL_DURATIONS[spell]))
        log(f'Player casts {spell}.')
        pass  # TODO
    elif spell == RECHARGE:
        pass  # TODO
    else:
        1/0


def check_gameover():
    if player.hp <= 0:
        print('The player dies.')
        exit()  # TODO?
    elif boss.hp <= 0:
        print('The boss dies.')
        exit()  # TODO?


def log_stats():
    log(f'- Player has {player.hp} hit points, {player.armor} armor, ' +
        f'{player.mana} mana')
    log(f'- Boss has {boss.hp} hit points')


def log(*args, **kwargs):
    print(*args, **kwargs)
    pass


if __name__ == '__main__':
    main()
