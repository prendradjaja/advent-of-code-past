import collections
from datetime import datetime

from progress import ProgressBar, human_readable


n = 5
n = 3012210


def main():
    starttime = datetime.now()
    elves = collections.deque(
        range(1, n+1)
    )
    progress = ProgressBar(n)
    while len(elves) > 1:
        first = elves.popleft()
        _ = elves.popleft()  # Discard the second elf
        elves.append(first)
        if len(elves) % 1123 == 0:
            progress.show(n - len(elves))
    progress.done()

    print('Answer:')
    print(elves[0])



if __name__ == '__main__':
    main()
