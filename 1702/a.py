answer = 0
for line in open('in').read().strip().splitlines():
    row = [int(n) for n in line.split()]
    answer += max(row) - min(row)
print(answer)
