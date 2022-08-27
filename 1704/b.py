import itertools

is_anagram = lambda a, b: sorted(a) == sorted(b)

answer = 0
for line in open('in').read().strip().splitlines():
    passphrase = line
    words = passphrase.split()
    valid = (
        len(words) == len(set(words))
        and not any(
            is_anagram(w1, w2)
            for w1, w2 in itertools.combinations(words, 2)
        )
    )
    answer += int(valid)
print(answer)
