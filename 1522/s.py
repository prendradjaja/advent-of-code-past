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

# How much armor Shield adds
SHIELD_AMOUNT = 7


def log(*args, **kwargs):
    # return
    print(*args, **kwargs)
    pass


def main():
    # # 953
    # game.player_turn(POISON)
    # game.player_turn(RECHARGE)
    # game.player_turn(SHIELD)
    # game.player_turn(MAGIC_MISSILE)
    #
    # game.player_turn(POISON)
    # game.player_turn(MAGIC_MISSILE)
    # game.player_turn(MAGIC_MISSILE)
    # game.player_turn(MAGIC_MISSILE)
    # game.player_turn(MAGIC_MISSILE)
    #
    # game.log_stats()

    # dfs((), 954, set())
    # dfs((), 953, set())
    # dfs((), 907, set())
    # dfs((), 855, set())

    # This is the strategy that my search found, with mana cost 854 (too low). I can see why it's wrong -- poison was cast while it was still active
    game = make_game()
    for spell in ('Poison', 'Recharge', 'Poison', 'Poison', 'Magic Missile', 'Magic Missile'):
        game.player_turn(spell)
        game.boss_turn()



# (first set every visited flag to false)
nodes = 0
def dfs(u, target, visited):
    global nodes
    nodes += 1

    if nodes % 10000 == 0:
        print(f'... {nodes:,}')

    if mana_spent(u) >= target:
        return

    game_result = evaluate_node(u)
    if game_result == LOSS:
        return
    elif game_result == WIN:
        print(f'Win found with {mana_spent(u)} mana spent: {u}')
        exit()

    visited.add(u)
    for v in neighbors(u):
        if v not in visited:
            dfs(v, target, visited)


def neighbors(strategy):
    game = make_game()
    for spell in strategy:
        game.player_turn(spell)
        game.boss_turn()
    return [
        strategy + (spell,)
        for spell in SPELLS
        if SPELL_COSTS[spell] <= game.player.mana
    ]


def mana_spent(strategy):
    # TODO I guess this is missing a case. You could win at the Effect Phase of
    # a player turn, so the last spell isn't actually cast yet.
    return sum(SPELL_COSTS[spell] for spell in strategy)


WIN = 1
LOSS = -1
UNFINISHED = 0
def evaluate_node(strategy):
    game = make_game()
    for spell in strategy:
        game.player_turn(spell)
        if game.is_game_over:
            return WIN if game.is_win else LOSS
        game.boss_turn()
        if game.is_game_over:
            return WIN if game.is_win else LOSS
    return UNFINISHED


def make_game():
    return Game(
        boss_hp = 55,
        boss_damage = 8,
        player_hp = 50,
        player_mana = 500,
    )


class Game:
    def __init__(self, *, boss_hp, boss_damage, player_hp, player_mana):
        self.boss = Fighter(boss_hp, boss_damage, 0, 0)
        self.player = Fighter(player_hp, 0, 0, player_mana)
        self.active_effects = []
        self.is_game_over = False
        self.is_win = False
        self.total_mana_spent = 0


    def player_turn(self, spell):
        assert not self.is_game_over
        assert spell in SPELLS

        log('-- Player turn --')
        self.log_stats()

        try:
            self.handle_effects()
            self.check_gameover()

            self.cast_spell(spell)
            self.check_gameover()
        except GameOver:
            pass

        log('')
        # if not self.is_game_over:
        #     self.boss_turn()


    def boss_turn(self):
        assert not self.is_game_over
        log('-- Boss turn --')
        self.log_stats()

        try:
            self.handle_effects()
            self.check_gameover()

            self.boss_attack()
            self.check_gameover()
        except GameOver:
            pass

        log('')


    def handle_effects(self):
        to_remove = []
        for effect in self.active_effects:
            expired = self.handle_effect(effect)
            if expired:
                to_remove.append(effect)

        for effect in to_remove:
            self.active_effects.remove(effect)


    def handle_effect(self, effect):
        '''
        Returns True if (and only if) the effect has now worn off.
        '''
        effect.timer -= 1

        if effect.name == SHIELD:
            log(f"{effect.name}'s timer is now {effect.timer}.")
        elif effect.name == POISON:
            damage = 3
            self.boss.hp -= damage
            log(f'{effect.name} deals {damage} damage; its timer is now {effect.timer}.')
        elif effect.name == RECHARGE:
            amount = 101
            self.player.mana += amount
            log(f'{effect.name} provides {amount} mana; its timer is now {effect.timer}.')
        else:
            1/0

        if effect.timer <= 0:
            if effect.name != SHIELD:
                log(f'{effect.name} wears off.')
            else:
                self.player.armor -= SHIELD_AMOUNT
                log(f'{effect.name} wears off, decreasing armor by {SHIELD_AMOUNT}.')
            return True
        else:
            return False


    def boss_attack(self):
        if self.player.armor:
            damage = max(self.boss.damage - self.player.armor, 1)
            log(f'Boss attacks for {self.boss.damage} - {self.player.armor} = {damage} damage!')
        else:
            damage = self.boss.damage
            log(f'Boss attacks for {damage} damage!')
        self.player.hp -= damage


    def cast_spell(self, spell):
        assert spell in SPELLS

        spell_cost = SPELL_COSTS[spell]
        assert self.player.mana >= spell_cost, 'TODO handle this case?'
        self.player.mana -= spell_cost
        self.total_mana_spent += spell_cost

        if spell == MAGIC_MISSILE:
            damage = 4
            self.boss.hp -= damage
            log(f'Player casts {spell}, dealing {damage} damage.')
        elif spell == DRAIN:
            amount = 2
            self.boss.hp -= amount
            self.player.hp += amount
            log(f'Player casts {spell}, dealing {amount} damage, and healing {amount} hit points.')
        elif spell == SHIELD:
            self.player.armor += SHIELD_AMOUNT
            self.active_effects.append(Effect(spell, SPELL_DURATIONS[spell]))
            log(f'Player casts {spell}, increasing armor by {SHIELD_AMOUNT}.')
        elif spell == POISON:
            self.active_effects.append(Effect(spell, SPELL_DURATIONS[spell]))
            log(f'Player casts {spell}.')
        elif spell == RECHARGE:
            self.active_effects.append(Effect(spell, SPELL_DURATIONS[spell]))
            log(f'Player casts {spell}.')
        else:
            1/0


    def check_gameover(self):
        if self.player.hp <= 0:
            log('The player dies.')
            self.is_game_over = True
            self.is_win = False
            raise GameOver()
        elif self.boss.hp <= 0:
            log('The boss dies.')
            # print('The boss dies. ✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅')
            self.is_game_over = True
            self.is_win = True
            raise GameOver()


    def log_stats(self):
        log(f'- Player has {self.player.hp} hit points, {self.player.armor} armor, ' +
            f'{self.player.mana} mana')
        log(f'- Boss has {self.boss.hp} hit points')
        # log(f'- Total mana spent: {self.total_mana_spent}')


class GameOver(Exception):
    pass


if __name__ == '__main__':
    main()
