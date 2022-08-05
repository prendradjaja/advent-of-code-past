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
    print(*args, **kwargs)
    pass


def main():
    # # Example 1
    # game = Game(
    #     boss_hp = 13,
    #     boss_damage = 8,
    #     player_hp = 10,
    #     player_mana = 250,
    # )
    # game.player_turn(POISON)
    # game.boss_turn()
    # game.player_turn(MAGIC_MISSILE)
    # game.boss_turn()

    # Example 2
    game = Game(
        boss_hp = 14,
        boss_damage = 8,
        player_hp = 10,
        player_mana = 250,
    )
    game.player_turn(RECHARGE)
    game.boss_turn()
    game.player_turn(SHIELD)
    game.boss_turn()



class Game:
    def __init__(self, *, boss_hp, boss_damage, player_hp, player_mana):
        self.boss = Fighter(boss_hp, boss_damage, 0, 0)
        self.player = Fighter(player_hp, 0, 0, player_mana)
        self.active_effects = []
        self.is_game_over = False


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

        if spell == MAGIC_MISSILE:
            damage = 4
            self.boss.hp -= damage
            log(f'Player casts {spell}, dealing {damage} damage.')
            pass  # TODO
        elif spell == DRAIN:
            pass  # TODO
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
            print('The player dies.')
            self.is_game_over = True
            raise GameOver()
        elif self.boss.hp <= 0:
            print('The boss dies.')
            self.is_game_over = True
            raise GameOver()


    def log_stats(self):
        log(f'- Player has {self.player.hp} hit points, {self.player.armor} armor, ' +
            f'{self.player.mana} mana')
        log(f'- Boss has {self.boss.hp} hit points')


class GameOver(Exception):
    pass


if __name__ == '__main__':
    main()
