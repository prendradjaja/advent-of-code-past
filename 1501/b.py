floor = 0

for i, ch in enumerate(open('input.txt').read().strip(), start=1):
    if ch == '(':
        floor += 1
    elif ch == ')':
        floor -= 1
    else:
        1/0
    if floor < 0:
        print(i)
        break
