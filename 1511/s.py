from string import ascii_lowercase

def main():
    '''
    >>> main()
    Answer for part 1: cqjxxyzz
    Answer for part 2: cqkaabcc
    '''
    current_password='cqjxjnds'
    nums = as_numbers(current_password)

    increment(nums)
    while not valid(nums):
        increment(nums)
    print('Answer for part 1:', from_numbers(nums))

    increment(nums)
    while not valid(nums):
        increment(nums)
    print('Answer for part 2:', from_numbers(nums))

def valid(password_nums):
    return (
        has_increasing_straight(password_nums) and
        has_no_iol(password_nums) and
        has_two_pairs(password_nums)
    )

def has_increasing_straight(password_nums):
    for a, b, c in consecutives(password_nums, 3):
        if a + 1 == b and b + 1 == c:
            return True
    return False

def has_no_iol(password_nums):
    for each in password_nums:
        if ascii_lowercase[each] in 'iol':
            return False
    return True

def has_two_pairs(password_nums):
    pairs = set()
    for a, b in consecutives(password_nums):
        if a == b:
            pairs.add(a)
            if len(pairs) == 2:
                return True
    return False

# mutates the argument
def increment(numbers):
    '''
    >>> increment([0, 0, 0])
    [0, 0, 1]
    >>> increment([0, 0, 25])
    [0, 1, 0]
    >>> increment([0, 25, 25])
    [1, 0, 0]
    '''
    radix = 26
    i = len(numbers) - 1
    while numbers[i] == 25:
        numbers[i] = 0
        i -= 1
    numbers[i] += 1
    return numbers

def as_numbers(password):
    '''
    >>> as_numbers('abcz')
    [0, 1, 2, 25]
    '''
    return list(ascii_lowercase.find(ch) for ch in password)

def from_numbers(password_nums):
    '''
    >>> from_numbers([0, 1, 2, 25])
    'abcz'
    '''
    return ''.join(ascii_lowercase[idx] for idx in password_nums)

def consecutives(seq, n=2, string=False):
    """
    >>> list(consecutives('abcd'))
    [('a', 'b'), ('b', 'c'), ('c', 'd')]
    >>> list(consecutives('abcd', string=True))
    ['ab', 'bc', 'cd']
    >>> list(consecutives('abcd', 3, string=True))
    ['abc', 'bcd']
    >>> list(consecutives('abcd', 5, string=True))
    []
    """
    prevs = []
    for item in seq:
        prevs.append(item)
        if len(prevs) == n:
            if not string:
                yield tuple(prevs)
            else:
                yield ''.join(prevs)
            prevs.pop(0)

if __name__ == '__main__':
    main()
