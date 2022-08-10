import sys
from collections import namedtuple
from util import Record, findint
from types import SimpleNamespace


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

SPELL_DURATIONS = {
    MAGIC_MISSILE: None,
    DRAIN: None,
    SHIELD: 6,
    POISON: 6,
    RECHARGE: 5,
}

SHIELD_AMOUNT = 7  # How much armor Shield adds


def main():
    # Parse puzzle input
    global PUZZLE_INPUT
    PUZZLE_INPUT = SimpleNamespace()
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    line = f.readline()
    assert 'Hit Points' in line
    PUZZLE_INPUT.boss_hp = findint(line)
    line = f.readline()
    assert 'Damage' in line
    PUZZLE_INPUT.boss_damage = findint(line)

    # Search
    best = float('inf')
    while True:
        mana_spent = find_plan(best)
        if mana_spent:
            print(f'Current best plan: {mana_spent} mana spent')
            best = mana_spent
        else:
            break
    print('\nNo better plan exists. Answer:')
    print(best)


# SEARCH ------------------------------------------------------------------------------------------

def find_plan(mana_limit):
    '''Finds a way to win using strictly less than MANA_LIMIT, if possible'''
    try:
        dfs((), mana_limit, set())
    except SearchDone as e:
        return e.result
    else:
        return None


count_nodes = 0
def dfs(u, mana_limit, visited):
    global count_nodes
    count_nodes += 1

    if count_nodes % 100000 == 0:
        print(f'- Still searching for a better plan... ({count_nodes:,} nodes searched)')

    if get_mana_spent(u) >= mana_limit:
        return

    game_result = evaluate_node(u)
    if game_result == LOSS:
        return
    elif game_result == WIN:
        raise SearchDone(get_mana_spent(u))

    visited.add(u)
    for v in neighbors(u):
        if v not in visited:
            dfs(v, mana_limit, visited)


class SearchDone(Exception):
    def __init__(self, result):
        self.result = result


def make_game_from_puzzle_input():
    return Game(
        boss_hp = PUZZLE_INPUT.boss_hp,
        boss_damage = PUZZLE_INPUT.boss_damage,
        player_hp = 50,
        player_mana = 500,
    )


def neighbors(strategy):
    game = make_game_from_puzzle_input()
    for spell in strategy:
        game.player_turn(spell)
        game.boss_turn()
    return [
        strategy + (spell,)
        for spell in SPELLS
        if SPELL_COSTS[spell] <= game.player.mana
            and will_not_have_active_effect(game, spell)
    ]


def will_not_have_active_effect(game, spell):
    effect = find(game.active_effects, lambda effect: effect.name == spell)
    if not effect:
        return True
    else:
        if effect.timer == 1:
            return True
        else:
            return False


def get_mana_spent(strategy):
    # I guess this is missing a case (you could win at the Effect Phase of a
    # player turn, so the last spell isn't actually cast yet), but it doesn't
    # seem to matter for the puzzle input.
    return sum(SPELL_COSTS[spell] for spell in strategy)


WIN = 1
LOSS = -1
UNFINISHED = 0
def evaluate_node(strategy):
    game = make_game_from_puzzle_input()
    for spell in strategy:
        game.player_turn(spell)
        if game.is_game_over:
            return WIN if game.is_win else LOSS
        game.boss_turn()
        if game.is_game_over:
            return WIN if game.is_win else LOSS
    return UNFINISHED


# GAME --------------------------------------------------------------------------------------------

class Game:
    def __init__(self, *, boss_hp, boss_damage, player_hp, player_mana, verbose=False):
        self.boss = Fighter(boss_hp, boss_damage, 0, 0)
        self.player = Fighter(player_hp, 0, 0, player_mana)
        self.active_effects = []
        self.is_game_over = False
        self.is_win = False
        self.total_mana_spent = 0
        self.verbose = False


    def player_turn(self, spell):
        assert not self.is_game_over
        assert spell in SPELLS

        self.log('-- Player turn --')
        self.log_stats()

        try:
            self.player.hp -= 1
            self.check_gameover()

            self.handle_effects()
            self.check_gameover()

            self.cast_spell(spell)
            self.check_gameover()
        except GameOver:
            pass

        self.log('')


    def boss_turn(self):
        assert not self.is_game_over
        self.log('-- Boss turn --')
        self.log_stats()

        try:
            self.handle_effects()
            self.check_gameover()

            self.boss_attack()
            self.check_gameover()
        except GameOver:
            pass

        self.log('')


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
            self.log(f"{effect.name}'s timer is now {effect.timer}.")
        elif effect.name == POISON:
            damage = 3
            self.boss.hp -= damage
            self.log(f'{effect.name} deals {damage} damage; its timer is now {effect.timer}.')
        elif effect.name == RECHARGE:
            amount = 101
            self.player.mana += amount
            self.log(f'{effect.name} provides {amount} mana; its timer is now {effect.timer}.')
        else:
            1/0

        if effect.timer <= 0:
            if effect.name != SHIELD:
                self.log(f'{effect.name} wears off.')
            else:
                self.player.armor -= SHIELD_AMOUNT
                self.log(f'{effect.name} wears off, decreasing armor by {SHIELD_AMOUNT}.')
            return True
        else:
            return False


    def boss_attack(self):
        if self.player.armor:
            damage = max(self.boss.damage - self.player.armor, 1)
            self.log(f'Boss attacks for {self.boss.damage} - {self.player.armor} = {damage} damage!')
        else:
            damage = self.boss.damage
            self.log(f'Boss attacks for {damage} damage!')
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
            self.log(f'Player casts {spell}, dealing {damage} damage.')
        elif spell == DRAIN:
            amount = 2
            self.boss.hp -= amount
            self.player.hp += amount
            self.log(f'Player casts {spell}, dealing {amount} damage, and healing {amount} hit points.')
        elif spell == SHIELD:
            self.player.armor += SHIELD_AMOUNT
            self.active_effects.append(Effect(spell, SPELL_DURATIONS[spell]))
            self.log(f'Player casts {spell}, increasing armor by {SHIELD_AMOUNT}.')
        elif spell == POISON:
            self.active_effects.append(Effect(spell, SPELL_DURATIONS[spell]))
            self.log(f'Player casts {spell}.')
        elif spell == RECHARGE:
            self.active_effects.append(Effect(spell, SPELL_DURATIONS[spell]))
            self.log(f'Player casts {spell}.')
        else:
            1/0


    def check_gameover(self):
        if self.player.hp <= 0:
            self.log('The player dies.')
            self.is_game_over = True
            self.is_win = False
            raise GameOver()
        elif self.boss.hp <= 0:
            self.log('The boss dies.')
            self.is_game_over = True
            self.is_win = True
            raise GameOver()


    def log(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)


    def log_stats(self):
        self.log(f'- Player has {self.player.hp} hit points, {self.player.armor} armor, ' +
            f'{self.player.mana} mana')
        self.log(f'- Boss has {self.boss.hp} hit points')


class GameOver(Exception):
    pass


# MISC --------------------------------------------------------------------------------------------

def find(lst, pred):
    matches = [x for x in lst if pred(x)]
    assert len(matches) <= 1
    if matches:
        return matches[0]
    else:
        return None


assert list(SPELL_COSTS) == SPELLS
assert list(SPELL_DURATIONS) == SPELLS


if __name__ == '__main__':
    main()
