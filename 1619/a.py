import collections
from datetime import datetime

from progress import ProgressBar, human_readable


n = 5
n = 3012210


Elf = collections.namedtuple('Elf', 'id presents')


def main():
    starttime = datetime.now()
    print('Initializing...')
    elves = collections.deque(
        Elf(i + 1, 1)
        for i in range(n)
    )
    print(f'  Done after {human_readable(datetime.now() - starttime)}.')
    print('\nSimulating...')
    progress = ProgressBar(n)
    while len(elves) > 1:
        first = elves.popleft()
        second = elves.popleft()
        elves.append(
            Elf(first.id, first.presents + second.presents)
        )
        if len(elves) % 1123 == 0:
            progress.show(n - len(elves))
    progress.done()

    print('\nAnswer:')
    print(elves[0].id)



if __name__ == '__main__':
    main()
