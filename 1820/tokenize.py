'''
Token types:

.
(
)
|
^
$
LETTERS
'''

def tokenize(text):
    return Tokenizer(text).tokenize()


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.current = 0

    def tokenize(self):
        tokens = []
        while not self._is_at_end():
            tokens.append(self._getToken())
        return tokens

    def _getToken(self):
        if self._check('^'):   return self._advance()
        elif self._check('$'): return self._advance()
        elif self._check('('): return self._advance()
        elif self._check(')'): return self._advance()
        elif self._check('|'): return self._advance()
        elif self._check('.'): return self._advance()
        elif self._peek() in 'NSEW':
            token = self._advance()
            while self._peek() in 'NSEW':
                token += self._advance()
            return token
        else:
            raise ValueError('Unexpected character: ' + self._peek())

    def _is_at_end(self):
        return self.current >= len(self.text)

    def _check(self, ch):
        return self.text[self.current] == ch

    def _advance(self):
        ch = self.text[self.current]
        self.current += 1
        return ch

    def _peek(self):
        return self.text[self.current]
