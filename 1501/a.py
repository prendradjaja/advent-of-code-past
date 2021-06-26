floor = 0

for ch in open('input.txt').read().strip():
    if ch == '(':
        floor += 1
    elif ch == ')':
        floor -= 1
    else:
        1/0

print(floor)
