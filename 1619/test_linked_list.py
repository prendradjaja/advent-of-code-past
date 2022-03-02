from b import LinkedList


def main():
    try:
        run_tests()
    except:
        print('Tests failed. First exception:\n')
        raise
    print('All tests passed.')


def run_tests():
    # Test append() and popleft()
    xs = LinkedList([1, 2])
    assert as_string(xs) == '[ 1 (2) ]'
    check_validity(xs)

    xs.append(3)
    assert as_string(xs) == '[ 1 (2) 3 ]'
    check_validity(xs)

    xs.append(4)
    assert as_string(xs) == '[ 1 2 (3) 4 ]'
    check_validity(xs)

    xs.append(5)
    assert as_string(xs) == '[ 1 2 (3) 4 5 ]'
    check_validity(xs)

    assert xs.popleft() == 1
    assert as_string(xs) == '[ 2 3 (4) 5 ]'
    check_validity(xs)

    assert xs.popleft() == 2
    assert as_string(xs) == '[ 3 (4) 5 ]'
    check_validity(xs)

    assert xs.popleft() == 3
    assert as_string(xs) == '[ 4 (5) ]'
    check_validity(xs)

    assert xs.popleft() == 4
    assert as_string(xs) == '[ (5) ]'
    check_validity(xs)

    assert xs.popleft() == 5
    assert as_string(xs) == '[ ]'
    check_validity(xs)

    xs.append(1)
    assert as_string(xs) == '[ (1) ]'
    check_validity(xs)

    xs.append(2)
    assert as_string(xs) == '[ 1 (2) ]'
    check_validity(xs)

    # Test popcenter()
    xs = LinkedList([1, 2, 3, 4, 5])
    assert as_string(xs) == '[ 1 2 (3) 4 5 ]'
    check_validity(xs)

    assert xs.popcenter() == 3
    assert as_string(xs) == '[ 1 2 (4) 5 ]'
    check_validity(xs)

    assert xs.popcenter() == 4
    assert as_string(xs) == '[ 1 (2) 5 ]'
    check_validity(xs)

    assert xs.popcenter() == 2
    assert as_string(xs) == '[ 1 (5) ]'
    check_validity(xs)

    assert xs.popcenter() == 5
    assert as_string(xs) == '[ (1) ]'
    check_validity(xs)

    assert xs.popcenter() == 1
    assert as_string(xs) == '[ ]'
    check_validity(xs)


def as_string(mylist):
    node = mylist.first
    result = '[ '
    while node:
        if node == mylist.center:
            result += f'({node.value}) '
        else:
            result += f'{node.value} '
        node = node.next
    result += ']'
    return result


def check_validity(mylist):
    if mylist.length == 0:
        assert not mylist.first
        assert not mylist.last
    else:
        assert mylist.first
        assert mylist.last

        node = mylist.first
        actual_length = 0
        while node:
            node = node.next
            actual_length += 1
        assert mylist.length == actual_length

        node = mylist.last
        actual_length = 0
        while node:
            node = node.prev
            actual_length += 1
        assert mylist.length == actual_length


if __name__ == '__main__':
    main()
