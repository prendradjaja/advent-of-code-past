import sys, collections


Node = collections.namedtuple('Node', 'children metas')


def main():
    f = open(sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1] != '-' else 'in')
    data = iter(int(n) for n in f.read().strip().split())
    root = parse(data)
    print(value(root))


def parse(data):
    childcount = next(data)
    metacount = next(data)
    children = [parse(data) for _ in range(childcount)]
    metas = [next(data) for _ in range(metacount)]
    return Node(children, metas)


def value(tree):
    if len(tree.children) == 0:
        return sum(tree.metas)
    else:
        result = 0
        for index in tree.metas:
            try:
                result += value(tree.children[index - 1])
            except IndexError:
                pass
        return result


if __name__ == '__main__':
    main()
