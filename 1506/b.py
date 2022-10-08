grid = {(x,y): 0 for x in range(1000) for y in range(1000)}

for line in open('in'):
    line = line.replace('turn ', 'turn-').replace(',', ' ')
    cmd, x1, y1, _, x2, y2 = line.split()
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    assert x2 >= x1 and y2 >= y1
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            if cmd == 'toggle':
                grid[(x, y)] += 2
            elif cmd == 'turn-on':
                grid[(x, y)] += 1
            elif cmd == 'turn-off':
                grid[(x, y)] = max(0, grid[(x, y)] - 1)

lit = 0
for _, value in grid.items():
    lit += value

print(lit)
