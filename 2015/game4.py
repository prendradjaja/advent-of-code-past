from tester import tester


def game(numbers):
    last_spoken = {}
    for i, n in enumerate(numbers, start=1):
        logvalue = n
        logprev = None
        logi = i
        yield n
        last_spoken[n] = i

    while True:
        i += 1
        if logprev is None:
            n = 0
        else:
            n = logi - logprev
        logvalue = n
        logprev = last_spoken.get(n, None)
        logi = i
        yield n
        last_spoken[n] = i

if __name__ == '__main__':
    tester(game)
