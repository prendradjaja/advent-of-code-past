def main():
    puzzle_input = 33100000
    max_elf = 10
    while True:
        print(f'Simulating with {max_elf} elves')
        houses = simulate(max_elf)
        for i, presents in enumerate(houses):
            if presents >= puzzle_input:
                print('Answer:', i)
                exit()
        max_elf *= 10


def simulate(max_elf):
    houses = [0] * (max_elf + 1)
    for e in range(1, max_elf + 1):  # For each elf
        for i in range(e, max_elf + 1, e):  # For each house the elf visits
            houses[i] += e * 10
    return houses


if __name__ == '__main__':
    main()
