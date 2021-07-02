import types
from tester import tester

def game(numbers):
    log = []
    last_spoken = {}
    for i, n in enumerate(numbers, start=1):
        log.append(obj(
            value = n,
            prev = None,
            i = i,
        ))
        yield n
        last_spoken[n] = i

    while True:
        i += 1
        if log[-1].prev is None:
            n = 0
        else:
            n = log[-1].i - log[-1].prev
        log.append(obj(
            value = n,
            prev = last_spoken.get(n, None),
            i = i,
        ))
        yield n
        last_spoken[n] = i

def obj(**kwargs):
    result = types.SimpleNamespace()
    for key, value in kwargs.items():
        setattr(result, key, value)
    return result

if __name__ == '__main__':
    tester(game)
