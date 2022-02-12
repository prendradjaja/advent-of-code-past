import sys


def main():
    start = 1,1

    # Puzzle input
    target = 31,39
    favnum = 1352

    # # Example puzzle input
    # favnum = 10
    # target = 7,4

    xmax = 50
    ymax = 50

    # Generate maze
    floorplan = {}
    for x in range(xmax+1):
        for y in range(ymax+1):
            pos = (x, y)
            bits = bin(x*x + 3*x + 2*x*y + y + y*y + favnum)[2:]
            is_even = len([b for b in bits if b == '1']) % 2 == 0
            floorplan[pos] = '.' if is_even else '#'

    # # Display maze
    # for y in range(ymax+1):
    #     row = ''
    #     for x in range(xmax+1):
    #         pos = (x, y)
    #         row += floorplan[pos]
    #     print(row)

    # Define BFS
    class SearchDone(Exception):
        pass
    parent = {}
    nearby = 0
    def pathlen(node):
        curr = node
        result = 0
        while curr != start:
            result += 1
            curr = parent[curr]
        return result
    def bfs(node, visited):
        visit(node, None)
        visited.add(node)
        q = [node]
        while q:
            node = q.pop(0)
            for v in neighbors(node):
                if v not in visited:
                    visit(v, node)
                    visited.add(v)
                    q.append(v)
    def visit(node, via):  # via = the node you're visiting from
        nonlocal nearby
        parent[node] = via
        mypathlen = pathlen(node)
        if mypathlen > 50:
            raise SearchDone()
        else:
            nearby += 1
    def neighbors(node):
        for offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nei = addvec(node, offset)
            x, y = nei
            if x >= 0 and y >= 0 and floorplan[nei] == '.':
                yield nei

    # Do BFS
    try:
        bfs(start, set())
    except SearchDone:
        pass
    print(nearby)


def addvec(a, b):
    return tuple(x+y for x,y in zip(a,b))


if __name__ == '__main__':
    main()
