def ilen_exhaustive(seq):
    """
    Given a finite iterator, return the number of items. As a necessary side
    effect, this also exhausts the iterator.
    >>> iterator = iter('abc')
    >>> ilen_exhaustive(iterator)
    3
    >>> ilen_exhaustive(iterator)
    0
    """
    count = 0
    for _ in seq:
        count += 1
    return count
