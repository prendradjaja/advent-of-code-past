answer = 0
for line in open('in').read().strip().splitlines():
    passphrase = line
    words = passphrase.split()
    valid = len(words) == len(set(words))
    answer += int(valid)
print(answer)
