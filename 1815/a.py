from collections import namedtuple
import math


ATTACK_POWER = 3
MAX_HIT_POINTS = 200

GOBLIN = 'G'
ELF = 'E'
UNIT_KINDS = (GOBLIN, ELF)
WALL = '#'

COMBAT_END = 'COMBAT_END'

DOUBLE_WIDE_RENDERING = True
DOUBLE_WIDE_RENDERING = False


def main():
    world = World(open('in').read())
    # world.show()

#     world = World('''
# #######
# #.G...#
# #...EG#
# #.#.#G#
# #..G#E#
# #.....#
# #######
#     '''.strip())

    while True:
        is_combat_end = bool(world.simulate_round())
        if is_combat_end:
            break
    print(world.get_outcome())


################################################################################


# When sorted, these come out in Reading Order.
Position = namedtuple('Position', 'r c')


class Unit:
    def __init__(self, kind):
        assert kind in UNIT_KINDS
        self.hit_points = MAX_HIT_POINTS
        self.kind = kind


class World:
    def __init__(self, text):
        self.walls = set()
        self.units = {}
        self.completed_rounds = 0
        for r, row in enumerate(text.splitlines()):
            for c, ch in enumerate(row):
                if ch == WALL:
                    self.walls.add(Position(r, c))
                elif ch in UNIT_KINDS:
                    self.units[Position(r, c)] = Unit(ch)

    def simulate_round(self):
        '''
        Returns None if the round completed normally, "COMBAT_END" if it ended
        early due to combat end.
        '''
        turn_order = sorted(self.units)
        for pos in turn_order:
            if pos not in self.units:
                # This unit must have been killed by a unit on a previous turn
                # within this round. Skip its turn.
                continue

            turn_result = self.take_turn(pos)
            if turn_result == COMBAT_END:
                return COMBAT_END
        self.completed_rounds += 1
        return None

    def take_turn(self, pos, *, _move_only=False):
        '''
        Given a unit (indicated by its Position), determine what that unit
        wants to do (and carry out that action(s): movement and/or attack).

        Returns None normally, except when combat ends (signaled by returning
        'COMBAT_END')
        '''

        def get_enemy_neighbor_positions(self, pos):
            result = []
            unit = self.units[pos]
            enemy_kind = other_kind(unit.kind)
            for neighbor in neighbors(pos):
                if isinstance(self.get(neighbor), Unit) and self.get(neighbor).kind == enemy_kind:
                    result.append(neighbor)
            return result

        ################################################################################

        assert pos in self.units

        # Check for combat end
        unit = self.units[pos]
        enemy_kind = other_kind(unit.kind)
        if not any(self.units[other_pos].kind == enemy_kind for other_pos in self.units):
            return COMBAT_END

        # Plan movement
        if get_enemy_neighbor_positions(self, pos):
            move_to = pos  # Don't move
        else:
            destination = self.choose_destination(pos)
            if not destination:
                # Can't attack and nowhere to move. End turn without doing
                # anything.
                return

            # Choose which square to MOVE_TO on this turn that would
            # eventually lead to DESTINATION.
            distances = self.get_distances(destination)
            move_to = min(
                self.empty_neighbors(pos),
                key = lambda neighbor: (distances.get(neighbor, math.inf), neighbor)
            )
            assert move_to in distances

        # Move
        unit = self.units.pop(pos)
        self.units[move_to] = unit
        pos = move_to

        if _move_only:
            return

        # Attack
        enemies = get_enemy_neighbor_positions(self, pos)
        if enemies:
            # Choose which enemy to attack
            enemy_pos = min(
                enemies,
                key = lambda pos: (self.get(pos).hit_points, pos)
            )

            # Actually attack
            enemy = self.get(enemy_pos)
            enemy.hit_points -= ATTACK_POWER
            if enemy.hit_points <= 0:
                del self.units[enemy_pos]

    def get_outcome(self):
        total_hit_points = 0
        for pos in self.units:
            total_hit_points += self.units[pos].hit_points

        return self.completed_rounds * total_hit_points

    def get(self, pos):
        '''
        Given a Position in the world, return WALL, Unit, or None depending on
        what is there.
        '''
        wall = WALL if pos in self.walls else None
        unit = self.units.get(pos, None)
        assert not (wall and unit)
        return wall or unit

    def is_empty(self, pos):
        return self.get(pos) is None

    def choose_destination(self, pos, *, _return_intermediate_results=False):
        '''
        Given a unit (indicated by its Position), determine its destination
        (where it wants to move to), as described in the spec ("To move, the
        unit first considers...").

        If there is NO destination possible, return None.

        In the example, the elf's destination is +:

        Targets:      In range:     Reachable:    Nearest:      Chosen:
        #######       #######       #######       #######       #######
        #E..G.#       #E.?G?#       #E.@G.#       #E.!G.#       #E.+G.#
        #...#.#  -->  #.?.#?#  -->  #.@.#.#  -->  #.!.#.#  -->  #...#.#
        #.G.#G#       #?G?#G#       #@G@#G#       #!G.#G#       #.G.#G#
        #######       #######       #######       #######       #######
        '''
        assert pos in self.units
        unit = self.units[pos]
        enemy_kind = other_kind(unit.kind)
        in_range = set()
        for other_pos, other_unit in self.units.items():
            if other_unit.kind == enemy_kind:
                for neighbor in self.empty_neighbors(other_pos):
                    in_range.add(neighbor)

        distances = self.get_distances(pos)
        reachable = { pos for pos in in_range if pos in distances }

        result = min(
            reachable,
            key = lambda pos: (distances[pos], pos),
            default = None,
        )

        if not _return_intermediate_results:  # The usual case
            return result
        else:
            return {
                'in-range': in_range,
                'reachable': reachable,
            }

    def empty_neighbors(self, pos):
        for neighbor in neighbors(pos):
            if self.is_empty(neighbor):
                yield neighbor

    def get_distances(self, p):
        '''
        Given a Position P, find every other Position Q that is reachable from
        P. Furthermore, for each Q, find Q's "shortest path distance" to P.

        Return a dict:
        { Q: SHORTEST_PATH_DISTANCE for every Q }
        '''
        def bfs(node):
            visit(node, None)
            visited.add(node)
            q = [node]
            while q:
                node = q.pop(0)
                for v in self.empty_neighbors(node):
                    if v not in visited:
                        visit(v, node)
                        visited.add(v)
                        q.append(v)
        def visit(node, parent):
            if node != p:
                assert parent in result
                result[node] = result[parent] + 1

        result = { p: 0 }
        visited = set()
        bfs(p)
        return result

    def show(self, *, with_hit_points=False):
        points = self.walls | set(self.units)
        min_r = min(p.r for p in points)
        max_r = max(p.r for p in points)
        min_c = min(p.c for p in points)
        max_c = max(p.c for p in points)
        for r in range(min_r, max_r + 1):
            units = []
            for c in range(min_c, max_c + 1):
                item = self.get(Position(r, c))
                if item is None:
                    ch = '.'
                elif item == WALL:
                    ch = WALL
                else:
                    ch = item.kind
                    units.append(item)
                print(ch, end=' ' if DOUBLE_WIDE_RENDERING else '')
            if with_hit_points:
                print('   ', end='')
                print(', '.join(f'{item.kind}({item.hit_points})' for item in units), end='')
            print()
        print()


def neighbors(pos):
    r, c = pos
    return [
        Position(r - 1, c),
        Position(r + 1, c),
        Position(r, c - 1),
        Position(r, c + 1),
    ]


def other_kind(kind):
    assert kind in UNIT_KINDS
    if kind == GOBLIN:
        return ELF
    elif kind == ELF:
        return GOBLIN
    else:
        raise Exception('unreachable case')


# def find_units(world):
#     for r, row in enumerate(world):
#         for c, ch in enumerate(row):
#             if ch in ['G', 'E']:


if __name__ == '__main__':
    main()
