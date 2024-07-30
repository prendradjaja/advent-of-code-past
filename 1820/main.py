from tokenize import tokenize
from parse import parse, Branch, Concatenation
from inputs import puzzle_input
from collections import defaultdict, deque


DIRECTIONS = {
    'N': (-1, 0),
    'S': (1, 0),
    'W': (0, -1),
    'E': (0, 1),
}


def main():
    text = puzzle_input

    text = text.replace('|)', '|.)')

    tokens = tokenize(text)
    tree = parse(tokens)

    graph = Graph()
    traverse(tree, graph, {(0, 0)})
    answer = max(graph.distances((0, 0)).values())
    print(answer)


class Graph:
    def __init__(self):
        self.edge_dict = defaultdict(set)

    def add_edge(self, v, w):
        self.edge_dict[v].add(w)
        self.edge_dict[w].add(v)

    # distances() implemented by generative AI
    def distances(self, start):
        # Initialize the queue with the start vertex and set its distance to 0
        queue = deque([start])
        distances = {start: 0}

        # Perform BFS
        while queue:
            current = queue.popleft()
            current_distance = distances[current]

            for neighbor in self.edge_dict[current]:
                if neighbor not in distances:  # If neighbor hasn't been visited
                    distances[neighbor] = current_distance + 1
                    queue.append(neighbor)

        return distances

    # show() implemented by generative AI
    def show(self):
        if not self.edge_dict:
            print("Graph is empty")
            return

        # Find the bounds of the graph
        min_row = min(v[0] for v in self.edge_dict)
        max_row = max(v[0] for v in self.edge_dict)
        min_col = min(v[1] for v in self.edge_dict)
        max_col = max(v[1] for v in self.edge_dict)

        # Initialize the grid with spaces
        row_count = (max_row - min_row + 1) * 2 - 1
        col_count = (max_col - min_col + 1) * 4 - 3
        grid = [[' ' for _ in range(col_count)] for _ in range(row_count)]

        # Place the vertices
        for (r, c) in self.edge_dict:
            grid[(r - min_row) * 2][(c - min_col) * 4] = '#'

        # Draw the edges
        for v, neighbors in self.edge_dict.items():
            r1, c1 = v
            for (r2, c2) in neighbors:
                if r1 == r2:  # Horizontal edge
                    row = (r1 - min_row) * 2
                    col_start = min(c1, c2) * 4 - min_col * 4
                    col_end = max(c1, c2) * 4 - min_col * 4
                    for i in range(col_start + 1, col_end):
                        grid[row][i] = '-'
                elif c1 == c2:  # Vertical edge
                    col = (c1 - min_col) * 4
                    row_start = min(r1, r2) * 2 - min_row * 2
                    row_end = max(r1, r2) * 2 - min_row * 2
                    for i in range(row_start + 1, row_end):
                        grid[i][col] = '|'

        # Print the grid
        for row in grid:
            print(''.join(row))


def traverse(tree_node, graph, positions):
    if isinstance(tree_node, Branch):
        return handle_branch(tree_node, graph, positions)
    elif isinstance(tree_node, Concatenation):
        return handle_concatenation(tree_node, graph, positions)
    elif tree_node == '.':
        return positions
    else:
        assert is_letters(tree_node)
        return handle_letters(tree_node, graph, positions)


def handle_letters(tree_node, graph, positions):
    ends = set()
    for start in positions:
        pos = start
        for ch in tree_node:
            new_pos = addvec(pos, DIRECTIONS[ch])
            graph.add_edge(pos, new_pos)
            pos = new_pos
        end = pos
        ends.add(end)
    return ends


def is_letters(tree_node):
    return isinstance(tree_node, str) and len(tree_node) >= 1 and set(tree_node) <= {*'NEWS'}


def handle_branch(tree_node, graph, positions):
    result = set()
    for child in tree_node.children:
        for start in positions:
            end = traverse(child, graph, {start})
            result |= end
    return result


def handle_concatenation(tree_node, graph, positions):
    for child in tree_node.children:
        new_positions = set()
        for pos in positions:
            new_positions |= traverse(child, graph, {pos})
        positions = new_positions
    return positions


def show_tree(tree, depth=0):
    indent = '  ' * depth
    if isinstance(tree, Branch):
        print(indent + 'Branch')
        for each in tree.children:
            show_tree(each, depth + 1)
    elif isinstance(tree, Concatenation):
        print(indent + 'Concatenation')
        for each in tree.children:
            show_tree(each, depth + 1)
    else:
        print(indent + tree)


def addvec(v, w):
    return tuple(a + b for a, b in zip(v, w))


if __name__ == '__main__':
    main()
