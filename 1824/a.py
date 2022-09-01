# Run as `python3 a.py | tail -n1` to avoid huge output

import re
from dataclasses import dataclass
from typing import List
from collections import Counter

IMMUNE_SYSTEM = 'Immune System'
INFECTION = 'Infection'

def main():
    text = open('in').read().strip()
    all_army_groups = parse_input(text)
    remaining_army_groups = all_army_groups[:]
    get_army_group = lambda group_id: [g for g in all_army_groups if g.get_id() == group_id][0]
    while not is_fight_over(remaining_army_groups):
        print_summary(remaining_army_groups)
        print()
        untargeted = remaining_army_groups[:]
        targets = {}

        # Select targets
        for group in sorted(
            remaining_army_groups,
            key = lambda g: (-g.effective_power(), -g.initiative)
        ):
            possible_targets = get_groups_in_team(
                untargeted,
                enemy_team(group.team_name)
            )
            if possible_targets:
                target = sorted(
                    possible_targets,
                    key = lambda t: (
                        -group.damage_vs_infinite_opponent(t),
                        -t.effective_power(),
                        -t.initiative
                    )
                )[0]
                targets[group.get_id()] = target
                untargeted.remove(target)

        # Attack
        for attacker_id in sorted(
            targets,
            key = lambda a_id: -get_army_group(a_id).initiative
        ):
            defender = targets[attacker_id]
            attacker = get_army_group(attacker_id)
            damage = attacker.damage_vs_infinite_opponent(defender)
            units_killed = defender.receive_damage(damage)
            print(
                f'{attacker.get_id()} attacks ' +
                f'defending {defender.name}, ' +  # e.g. "defending group 1,"
                f'killing {units_killed} units'
            )
            if defender.units == 0:
                remaining_army_groups.remove(defender)
        print()
        print('----')
        print()

    print_summary(remaining_army_groups)

    print()
    print('----')
    print()

    answer = sum([g.units for g in remaining_army_groups])
    print(answer)

def enemy_team(team):
    if team == IMMUNE_SYSTEM:
        return INFECTION
    elif team == INFECTION:
        return IMMUNE_SYSTEM
    else:
        assert False, 'Invalid team'

def get_groups_in_team(army_groups, team):
    return [g for g in army_groups if g.team_name == team]

def print_summary(army_groups):
    for team in [IMMUNE_SYSTEM, INFECTION]:
        print(team + ':')
        groups_in_team = get_groups_in_team(army_groups, team)
        if not groups_in_team:
            print('No groups remain.')
        else:
            for g in groups_in_team:
                print(g.short_summary())

def is_fight_over(army_groups):
    teams_alive = set(g.team_name for g in army_groups)
    return len(teams_alive) < 2

@dataclass
class ArmyGroup:
    team_name: str
    name: str
    units: int
    hit_points: int
    weaknesses: List[str]
    immunities: List[str]
    attack_type: str
    attack_damage: int
    initiative: int

    def get_id(self):
        return self.team_name + ' ' + self.name

    def effective_power(self):
        return self.units * self.attack_damage

    def damage_vs_infinite_opponent(self, opponent):
        if self.attack_type in opponent.immunities:
            return 0
        elif self.attack_type in opponent.weaknesses:
            return self.effective_power() * 2
        else:
            return self.effective_power()

    def receive_damage(self, damage):
        '''
        >>> g = ArmyGroup(
        ...     units = 100,
        ...     hit_points = 10,
        ...     team_name=None, name=None, weaknesses=None, immunities=None, attack_type=None, attack_damage=None, initiative=None,
        ... )
        >>> g.receive_damage(75)
        7
        >>> g.units
        93
        '''
        units_killed = min(damage // self.hit_points, self.units)
        self.units -= units_killed
        return units_killed

    def short_summary(self):
        capitalized_name = self.name[0].upper() + self.name[1:]
        return f'{capitalized_name} contains {self.units} units'

    def long_summary(self):
        return (
            f'{self.units} units each with ' +
            f'{self.hit_points} hit points ' +
            self._paren_text() +
            f'with an attack that does {self.attack_damage} {self.attack_type} damage ' +
            f'at initiative {self.initiative}'
        )

    def _paren_text(self):
        if not self.weaknesses and not self.immunities:
            return ''

        segments = []
        if self.immunities:
            segments.append('immune to ' + ', '.join(self.immunities))
        if self.weaknesses:
            segments.append('weak to ' + ', '.join(self.weaknesses))
        return '(' + '; '.join(segments) + ') '

def parse_input(text):
    '''
    >>> text = """
    ... Immune System:
    ... 17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
    ... 989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3
    ...
    ... Infection:
    ... 801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
    ... 4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
    ... """.strip()

    >>> for each in parse_input(text):
    ...     print(each.team_name, each.name, each.long_summary(), sep='|')
    Immune System|group 1|17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
    Immune System|group 2|989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3
    Infection|group 1|801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
    Infection|group 2|4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
    '''
    sections = text.split('\n\n')
    result = []
    for section in sections:
        team_name, *groups = section.strip().splitlines()
        team_name = team_name.rstrip(':')
        for i, line in enumerate(groups, start=1):
            attack_damage, attack_type = re.search(r'does (\d+) ([a-z]+) damage', line).groups()
            attack_damage = int(attack_damage)
            result.append(
                ArmyGroup(
                    team_name = team_name,
                    name = f'group {i}',
                    units = int(re.search(r'(\d+) units', line).group(1)),
                    hit_points = int(re.search(r'(\d+) hit points', line).group(1)),
                    weaknesses = parse_weaknesses(line),
                    immunities = parse_immunities(line),
                    attack_type = attack_type,
                    attack_damage = attack_damage,
                    initiative = int(re.search(r'initiative (\d+)', line).group(1)),
                )
            )
    return result

def parse_weaknesses(line, *, descriptor='weak to '):
    '''
    >>> parse_weaknesses('blah blah (weak to radiation, bludgeoning) blah blah')
    ['radiation', 'bludgeoning']
    >>> parse_weaknesses('(weak to radiation)')
    ['radiation']
    >>> parse_weaknesses('(immune to radiation; weak to fire, cold)')
    ['fire', 'cold']
    '''
    if descriptor not in line:
        return []
    paren_text = re.search(r'\(.*\)', line).group(0).lstrip('(').rstrip(')')
    segments = paren_text.split('; ')
    segment = [s for s in segments if s.startswith(descriptor)][0]
    return segment[len(descriptor):].split(', ')

def parse_immunities(paren_text):
    '''
    >>> parse_immunities('(weak to radiation, bludgeoning)')
    []
    >>> parse_immunities('(immune to fire; weak to bludgeoning, slashing)')
    ['fire']
    '''
    return parse_weaknesses(paren_text, descriptor='immune to ')

if __name__ == '__main__':
    main()
