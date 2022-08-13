import string
import sys
import collections
from datetime import datetime, timedelta

from util import findint


def main():
    input_file_path = sys.argv[1] if len(sys.argv) > 1 else 'in'
    grid, letter_to_guard = make_grid(input_file_path)

    show_grid(grid, monochrome=True)
    show_grid(grid)

    part_1_answer = solve_part_1(grid, letter_to_guard)
    print('Part 1 answer:', part_1_answer)

    part_2_answer = solve_part_2(grid, letter_to_guard)
    print('Part 2 answer:', part_2_answer)


def make_grid(input_file_path):
    f = open(input_file_path)
    lines = [l.rstrip('\n') for l in f]
    lines.sort()
    log = {}
    for i, line in enumerate(lines):
        parsed = parse_line(line)
        lines[i] = parsed
        log[parsed.timestamp] = parsed

    curr_time = lines[0].timestamp
    end_time = lines[-1].timestamp
    curr_guard = None
    grid = collections.defaultdict(dict)
    guard_letters = {}
    letters = iter(string.ascii_lowercase[:25])
    is_asleep = None
    while curr_time <= end_time:
        if curr_time in log:
            entry = log[curr_time]
            if entry.type == BEGINS_SHIFT:
                is_asleep = False
                curr_guard = entry.guard
                if curr_guard not in guard_letters:
                    guard_letters[curr_guard] = next(letters)
            elif entry.type == FALLS_ASLEEP:
                is_asleep = True
            elif entry.type == WAKES_UP:
                is_asleep = False
            else:
                1/0
        if curr_time.hour == 0:
            date = curr_time.strftime('%m-%d')
            minute = curr_time.strftime('%M')
            letter = guard_letters[curr_guard]
            if is_asleep:
                letter = letter.upper()
            grid[date][minute] = letter
        curr_time += timedelta(minutes=1)

    letter_to_guard = {v: k for k, v in guard_letters.items()}

    return grid, letter_to_guard


def solve_part_1(grid, letter_to_guard):
    minutes_asleep_by_guard = collections.Counter()
    for date in sorted(grid):
        for minute in grid[date]:
            entry = grid[date][minute]
            if entry.isupper():
                minutes_asleep_by_guard[entry] += 1
    sleepiest_guard_letter = minutes_asleep_by_guard.most_common(1)[0][0].lower()
    sleepiest_guard_number = letter_to_guard[sleepiest_guard_letter]

    times_asleep_by_minute = collections.Counter()
    for date in sorted(grid):
        for minute in grid[date]:
            entry = grid[date][minute]
            guard_letter = entry.lower()
            if guard_letter == sleepiest_guard_letter and entry.isupper():
                times_asleep_by_minute[int(minute)] += 1
    sleepiest_minute = times_asleep_by_minute.most_common(1)[0][0]
    return sleepiest_minute * sleepiest_guard_number


def solve_part_2(grid, letter_to_guard):
    times_asleep_by_guard_minute = collections.Counter()
    for date in sorted(grid):
        for minute in grid[date]:
            entry = grid[date][minute]
            guard_number = letter_to_guard[entry.lower()]
            minute = int(minute)
            if entry.isupper():
                times_asleep_by_guard_minute[(guard_number, minute)] += 1
    guard, minute = times_asleep_by_guard_minute.most_common(1)[0][0]
    return guard * minute


def show_grid(grid, *, monochrome=False):
    ROW_LIMIT = 5
    print('''
Date   Minute
       000000000011111111112222222222333333333344444444445555555555
       012345678901234567890123456789012345678901234567890123456789
    '''.strip())
    dates = sorted(grid)
    for i, date in enumerate(dates):
        if i >= ROW_LIMIT:
            print(f'({len(dates) - ROW_LIMIT} more rows)')
            break
        row = f'{date}  '
        for minute in grid[date]:
            entry = grid[date][minute]
            if monochrome:
                entry = '#' if entry.isupper() else '.'
            row += entry
        print(row)
    print()


LogEntry = collections.namedtuple('LogEntry', 'timestamp type guard')
BEGINS_SHIFT = 'BEGINS_SHIFT'
FALLS_ASLEEP = 'FALLS_ASLEEP'
WAKES_UP = 'WAKES_UP'
def parse_line(line):
    timestamp = parse_timestamp(line.split(']')[0][1:])
    if 'begins shift' in line:
        guard = findint(line.split('#')[1])
        return LogEntry(timestamp, BEGINS_SHIFT, guard)
    elif 'falls asleep' in line:
        return LogEntry(timestamp, FALLS_ASLEEP, None)
    elif 'wakes up' in line:
        return LogEntry(timestamp, WAKES_UP, None)


def parse_timestamp(timestamp):
    parts = timestamp.replace('-', ' ').replace(':', ' ').split()
    year, month, day, hour, minute = [int(n) for n in parts]
    return datetime(year, month, day, hour, minute)


if __name__ == '__main__':
    main()
