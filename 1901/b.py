def fuel(mass):
    fuel_mass = max(mass // 3 - 2, 0)
    if fuel_mass:
        return fuel_mass + fuel(fuel_mass)
    else:
        return 0

masses = [int(n) for n in open('in')]
print(sum(fuel(m) for m in masses))
