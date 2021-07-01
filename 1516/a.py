from util import *

gifter_raw_data = '''
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
'''

def parse_sue(raw_data):
    data = {}
    for datum in raw_data:
        key, value = datum.strip().split(': ')
        value = int(value)
        data[key] = value
    return data

def main():
    gifter = parse_sue(gifter_raw_data.strip().split('\n'))

    def matches_gifter(sue):
        for key in sue:
            if sue[key] != gifter[key]:
                return False
        return True

    sues = {}
    for line in open('input.txt'):
        left, right = line.split(':', maxsplit=1)
        i = findint(left)
        sues[i] = parse_sue(right.strip().split(','))

    for i in sues:
        if matches_gifter(sues[i]):
            print(i)

if __name__ == '__main__':
    main()
