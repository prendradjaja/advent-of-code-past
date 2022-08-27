fuel = lambda mass: mass // 3 - 2
masses = [int(n) for n in open('in')]
print(sum(fuel(m) for m in masses))
