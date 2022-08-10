# Use `from b import ...` for hard mode
from a import Game, POISON, MAGIC_MISSILE


game = Game(
    boss_hp = 13,
    boss_damage = 8,
    player_hp = 10,
    player_mana = 250,
    verbose = True,
)

game.player_turn(POISON)
game.boss_turn()
game.player_turn(MAGIC_MISSILE)
game.boss_turn()
