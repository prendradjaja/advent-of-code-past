def main():
    text = open('in').read().strip()
    deck = shuffle(text, 10007)
    answer = deck.index(2019)
    print(answer)

def shuffle(text, deck_size):
    '''
    >>> shuffle('cut 2', 5)
    [2, 3, 4, 0, 1]

    >>> shuffle('cut -2', 5)
    [3, 4, 0, 1, 2]

    >>> text = """
    ... deal with increment 7
    ... deal into new stack
    ... deal into new stack
    ... """.strip()
    >>> shuffle(text, 10)
    [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]

    >>> text = """
    ... cut 6
    ... deal with increment 7
    ... deal into new stack
    ... """.strip()
    >>> shuffle(text, 10)
    [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
    '''
    deck = list(range(deck_size))
    for line in text.splitlines():
        if line.startswith('cut'):
            n = int(line.split()[-1])
            deck = deck[n:] + deck[:n]
        elif line == 'deal into new stack':
            deck = deck[::-1]
        elif line.startswith('deal with increment'):
            n = int(line.split()[-1])
            j = 0
            new_deck = [None] * deck_size
            for i in range(deck_size):
                new_deck[j] = deck[i]
                deck[i] = None
                j = (j + n) % deck_size
            deck = new_deck
            assert None not in deck
    return deck

if __name__ == '__main__':
    main()
