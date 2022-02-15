# There are several progress bars available. Use ACTIVE_PROGRESS_BAR to choose.

import sys
from progress import ProgressBar, ProgressPrinter
import math


ACTIVE_PROGRESS_BAR = 'lin'       # Current length of the dragon
# ACTIVE_PROGRESS_BAR = 'log'       # Current length of the dragon (log scale)
# ACTIVE_PROGRESS_BAR = 'steps'     # Current iteration
# ACTIVE_PROGRESS_BAR = 'print'     # Not a progress bar: Simply print()


def main():
    puzzle_input = '11100010111110100'
    disk_size = 35651584
    # disk_size = 3565152  # Smaller example

    dragon_progress = MultiProgress({
        'log': ProgressBar(math.ceil(math.log10(disk_size))),
        'lin': ProgressBar(disk_size),
        'steps': ProgressBar(None, width=40, indeterminate_scale=20),
        'print': ProgressPrinter(),
    })
    dragon_progress.activate(ACTIVE_PROGRESS_BAR)

    text = puzzle_input

    print('Creating dragon:')
    step = 1
    while len(text) < disk_size:
        text = dragon_step(text)
        dragon_progress.show({
            'log': math.ceil(math.log10(len(text))),
            'lin': len(text),
            'steps': step,
            'print': f'Dragon length: {len(text):,}',
        })
        step += 1
    dragon_progress.done()


    # Compute checksum
    print('Computing checksum:')
    global checksum_progress
    global checksum_step
    checksum_progress = ProgressBar(None, indeterminate_scale=12)
    checksum_step = 1
    text = text[:disk_size]
    answer = checksum(text)
    checksum_progress.done()
    print('Answer:', str(answer)[:10] + ('...' if len(str(answer)) > 10 else ''))


def dragon_step(a):
    b = ''.join(reversed(a))
    b = invert(b)
    return a + '0' + b


def invert(s):
    result = ''
    for ch in s:
        assert ch in '01'
        other = '1' if ch == '0' else '0'
        result += other
    return result


def checksum(text):
    global checksum_step
    checksum_progress.show(checksum_step)
    checksum_step += 1
    assert len(text) % 2 == 0
    result = ''
    for i in range(0, len(text), 2):
        pair = text[i : i+2]
        left, right = pair
        result += str(int(bool(left == right)))  # '0' or '1'
    if len(result) % 2 == 1:
        return result
    else:
        return checksum(result)


class MultiProgress:
    def __init__(self, progress_bars):
        self.progress_bars = progress_bars
        self.active = None

    def activate(self, key):
        self.active = key

    def show(self, values):
        if self.active:
            self.progress_bars[self.active].show(values[self.active])

    def done(self):
        if self.active:
            self.progress_bars[self.active].done()


if __name__ == '__main__':
    main()
