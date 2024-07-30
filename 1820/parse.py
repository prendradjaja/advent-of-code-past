'''
Grammar:

program =
  "^" expression "$"

expression =
  branch

branch =
  concatenation ("|" concatenation)*

concatenation =
  primary primary*

primary =
  LETTERS
  "(" expression ")"
'''

from collections import namedtuple


Branch = namedtuple('Branch', 'children')
Concatenation = namedtuple('Concatenation', 'children')


def parse(tokens):
    return Parser(tokens).parse()


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self._program()

    def _program(self):
        if not self._match('^'):
            raise ValueError('Expected ^, got ' + self._peek())
        result = self._expression()
        if not self._match('$'):
            raise ValueError('Expected $, got ' + self._peek())
        return result

    def _expression(self):
        return self._branch()

    def _branch(self):
        children = [self._concatenation()]
        while self._check('|'):
            self._advance()
            children.append(self._concatenation())
        return Branch(tuple(children))

    def _concatenation(self):
        children = [self._primary()]
        while (
            self._check('LETTERS')
            or self._check('(')
            or self._check('.')
        ):
            children.append(self._primary())
        return Concatenation(tuple(children))

    def _primary(self):
        if self._check('.'):
            return self._advance()
        elif self._check('LETTERS'):
            return self._advance()
        elif self._check('('):
            self._advance()
            result = self._expression()
            if not self._match(')'):
                raise ValueError('Expected )')
            return result
        else:
            raise ValueError('Unexpected token in _primary(): ' + self._peek())

    def _is_at_end(self):
        return self.current >= len(self.tokens)

    def _check(self, token_type):
        '''
        token_type: "^" | "$" | "(" | ")" | "|" | "." | "LETTERS"
        '''
        token = self._peek()
        if token == token_type:
            return True
        is_letters_type = set(token) <= {*'NEWS'}
        if token_type == 'LETTERS' and is_letters_type:
            return True
        return False

    def _match(self, token_type):
        '''
        token_type: "^" | "$" | "(" | ")" | "|" | "." | "LETTERS"

        Returns: bool
        '''
        if self._check(token_type):
            self._advance()
            return True
        return False

    def _advance(self):
        token = self.tokens[self.current]
        self.current += 1
        return token

    def _peek(self):
        return self.tokens[self.current]
