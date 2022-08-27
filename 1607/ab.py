def main():
    ips = [line for line in open('in').read().strip().splitlines()]

    answer1 = sum([1 for ip in ips if supports_tls(ip)])
    print('Part 1 answer:', answer1)

    answer2 = sum([1 for ip in ips if supports_ssl(ip)])
    print('Part 2 answer:', answer2)


def supports_tls(ip):
    '''
    >>> supports_tls('abba[mnop]qrst')
    True
    >>> supports_tls('abcd[bddb]xyyx')
    False
    >>> supports_tls('aaaa[qwer]tyui')
    False
    >>> supports_tls('ioxxoj[asdfgh]zxcvbn')
    True
    '''
    return bool(
        find_abbas(ip)
        and all(not find_abbas(hns) for hns in hypernet_sequences(ip))
    )


def supports_ssl(ip):
    '''
    >>> supports_ssl('aba[bab]xyz')
    True
    >>> supports_ssl('xyx[xyx]xyx')
    False
    >>> supports_ssl('aaa[kek]eke')
    True
    >>> supports_ssl('zazbz[bzb]cdb')
    True
    '''
    all_abas = []
    for sns in supernet_sequences(ip):
        all_abas.extend(find_abas(sns))

    if not all_abas:
        return False

    for aba in all_abas:
        bab = get_bab(aba)
        if any(
            bab in hns
            for hns in hypernet_sequences(ip)
        ):
            return True
    return False


def find_abbas(s):
    '''
    >>> find_abbas('xyzabbaxyz')
    ['abba']
    >>> find_abbas('xyzaaaaxyz')
    []
    '''
    result = []
    for a, b, c, d in zip(s, s[1:], s[2:], s[3:]):
        if a != b == c != d == a:
            result.append(a + b + c + d)
    return result


def find_abas(s):
    '''
    >>> find_abas('xyzabaxyz')
    ['aba']
    >>> find_abas('xyzaaaxyz')
    []
    '''
    result = []
    for a, b, c in zip(s, s[1:], s[2:]):
        if a != b != c == a:
            result.append(a + b + c)
    return result


def get_bab(aba):
    a, b, c = aba
    assert a == c
    return b + a + b


def hypernet_sequences(s, *, start_char='[', end_char=']'):
    '''
    >>> hypernet_sequences('abc[def]ghi[jkl]mno')
    ['def', 'jkl']
    >>> hypernet_sequences('[def]ghi[jkl]')
    ['def', 'jkl']
    >>> hypernet_sequences('abcdef')
    []
    >>> hypernet_sequences('[abcdef]')
    ['abcdef']
    '''
    result = []
    current_item = None
    for ch in s:
        if ch == start_char:
            current_item = ''
        elif ch == end_char:
            if current_item:
                result.append(current_item)
            current_item = None
        elif current_item is not None:
            current_item += ch
    return result


def supernet_sequences(s):
    '''
    >>> supernet_sequences('abc[def]ghi')
    ['abc', 'ghi']
    >>> supernet_sequences('[abc]def[ghi]')
    ['def']
    >>> supernet_sequences('[abc]')
    []
    >>> supernet_sequences('abc')
    ['abc']
    '''
    return hypernet_sequences(
        ']' + s + '[',
        start_char = ']',
        end_char = '['
    )


if __name__ == '__main__':
    main()
