import sys
import re


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')

    initial_password = 'abcdefgh'
    password = list(initial_password)
    lines = [l.rstrip('\n') for l in f]

    for line in lines:
        if args := sscanf(line, 'swap position %u with position %u'):
            i, j = args
            password[i], password[j] = password[j], password[i]
        elif args := sscanf(line, 'swap letter %s with letter %s'):
            a, b = args
            i = password.index(a)
            j = password.index(b)
            password[i], password[j] = password[j], password[i]
        elif (
            (args := sscanf(line, 'rotate %s %u steps'))
            or (args := sscanf(line, 'rotate %s %u step'))
        ):
            direction, unsigned_steps = args
            if direction == 'left':
                steps = -unsigned_steps
            elif direction == 'right':
                steps = unsigned_steps
            else:
                1/0  # Invalid rotation direction
            password = rotate_right(password, steps)
        elif args := sscanf(line, 'rotate based on position of letter %s'):
            (letter,) = args
            index = password.index(letter)
            maybe_extra = 1 if index >= 4 else 0
            password = rotate_right(password, 1 + index + maybe_extra)
        elif args := sscanf(line, 'reverse positions %u through %u'):
            start, end = args
            password = reverse_substring(password, start, end)
        elif args := sscanf(line, 'move position %u to position %u'):
            src, dest = args
            password = move_char(password, src, dest)
        else:
            1/0  # Invalid instruction

    print(''.join(password))


def move_char(s, src, dest):
    '''
    >>> move_char('abcde', 0, 4)
    'bcdea'
    >>> move_char('abcde', 4, 0)
    'eabcd'
    >>> move_char('abcde', 1, 3)
    'acdbe'

    Also works on tuples and lists
    >>> move_char(tuple('abcde'), 1, 3) == tuple('acdbe')
    True
    '''
    ch = s[src]
    ch = type(s)(ch)
    s = s[:src] + s[src+1:]
    return s[:dest] + ch + s[dest:]


def rotate_right(s, steps):
    '''
    >>> rotate_right('abcde', -2)
    'cdeab'
    >>> rotate_right('abcde', 2)
    'deabc'
    >>> rotate_right('abcde', 0)
    'abcde'

    Also works on tuples and lists
    >>> rotate_right(list('abcde'), 2) == list('deabc')
    True
    >>> rotate_right(tuple('abcde'), 2) == tuple('deabc')
    True
    '''
    steps = steps % len(s)
    if steps > 0:
        return s[-steps:] + s[:-steps]
    else:
        return s


def reverse_substring(s, start, end_inclusive):
    '''
    >>> reverse_substring('abcde', 0, 4)
    'edcba'
    >>> reverse_substring('Hello abcde !?', 6, 10)
    'Hello edcba !?'

    Also works on tuples and lists
    >>> reverse_substring(tuple('Hello abcde !?'), 6, 10) == tuple('Hello edcba !?')
    True
    '''
    end_exclusive = end_inclusive + 1
    return s[:start] + s[start:end_exclusive][::-1] + s[end_exclusive:]


def sscanf(s, fmt):
    '''
    Parses the string against the given template, returning the values of the
    slots. If no match, return None.

    The string must be a full match (like re.fullmatch()).

    Each slot is parsed non-greedily. (Is this a good approach?)

    Supported placeholders:
    %s: Scan a string. Unlike C sscanf(), the scan is not terminated at
        whitespace.
    %u: Scan for a positive ("unsigned") decimal integer.

    TODO Add support for %d

    >>> sscanf(
    ...     'The quick brown fox jumped over 2 lazy dogs',
    ...     'The %s brown fox jumped over %u lazy dogs',
    ... )
    ('quick', 2)

    >>> sscanf(
    ...     'quick fox, 2 dogs, 31 cats, wow!',
    ...     '%s fox, %u dogs, %u cats, %s',
    ... )
    ('quick', 2, 31, 'wow!')

    >>> sscanf(
    ...     'quick fox, 2 dogs, 31 cats',
    ...     '%s fox, %u dogs, %u cats, %s',
    ... ) == None
    True
    '''
    # Parse `fmt` into `pattern`
    slot_pattern = r'(%s|%u)'
    pattern = ''
    slot_types = []
    for part in re.split(slot_pattern, fmt):
        is_slot = bool(re.fullmatch(slot_pattern, part))
        if is_slot:
            slot_types.append(part)
            if part == '%s':
                pattern += r'(.+?)'
            elif part == '%u':
                pattern += r'(\d+?)'
            else:
                1/0  # Invalid placeholder
        else:
            pattern += re.escape(part)

    # Try to match
    match = re.fullmatch(pattern, s)
    if not match:
        return None

    # If match, parse values and return
    result = ()
    for raw_value, slot_type in zip(match.groups(), slot_types):
        if slot_type == '%s':
            value = raw_value
        elif slot_type == '%u':
            value = int(raw_value)
        result += (value,)
    return result


if __name__ == '__main__':
    main()
