def find_start(nodes):
    y = 0
    x = max(x for x, y in nodes)
    return x, y


def show_histogram(data):
    count_buckets = 10
    data = list(data)
    lo = min(data)
    hi = max(data)
    bucket_size = (hi - lo) / count_buckets
    buckets = defaultdict(list)
    for i in range(1, count_buckets + 1):
        cutoff = lo + i * bucket_size
        if i == count_buckets:
            assert cutoff == hi
        buckets[cutoff]
        for j in reversed(range(len(data))):
            if data[j] <= cutoff:
                buckets[cutoff].append(data.pop(j))
    for cutoff, items in buckets.items():
        print(f'<= {cutoff}:\t {len(items)}')


def analyze(nodes):
    verbose = True
    count_empty_nodes = sum(
        1
        for node in nodes.values()
        if node.used == 0
    )
    assert count_empty_nodes == 1
    print('There is exactly one empty node')

    median_size = statistics.median([node.size for node in nodes.values()])
    count_small_nodes = sum(
        1
        for node in nodes.values()
        if node.size < 2 * median_size
        and node.used != 0
    )
    count_large_nodes = sum(
        1
        for node in nodes.values()
        if node.size > 3 * median_size
        and node.used != 0
    )
    size_cutoff = 2.5 * median_size
    assert count_empty_nodes + count_small_nodes + count_large_nodes == len(nodes)
    print('The rest of the nodes are distinctly either "small" nodes or "large" nodes, with nothing in between')

    start = find_start(nodes)
    end = (0, 0)

    assert nodes[start].size < size_cutoff and nodes[end].size < size_cutoff
    print('The start and end nodes are both small nodes')

    return size_cutoff
