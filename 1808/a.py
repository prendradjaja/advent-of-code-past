import sys


def main():
    f = open(sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1] != '-' else 'in')
    data = iter(int(n) for n in f.read().strip().split())
    metas = []
    parse(data, metas)
    print(sum(metas))


def parse(data, metas):
    childcount = next(data)
    metacount = next(data)
    for _ in range(childcount):
        parse(data, metas)
    for _ in range(metacount):
        metas.append(next(data))



if __name__ == '__main__':
    main()
