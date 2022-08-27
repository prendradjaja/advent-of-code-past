program = [int(line) for line in open('in').read().strip().splitlines()]
ip = 0
steps = 0
while 0 <= ip < len(program):
    offset = program[ip]
    program[ip] += 1
    ip += offset
    steps += 1
print(steps)
