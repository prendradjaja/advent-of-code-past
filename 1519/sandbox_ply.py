# -----------------------------------------------------------------------------
# example.py
#
# Example of using PLY To parse the following simple grammar.
#
#   expression : term PLUS term
#              | term MINUS term
#              | term
#
#   term       : factor TIMES factor
#              | factor DIVIDE factor
#              | factor
#
#   factor     : NUMBER
#              | NAME
#              | PLUS factor
#              | MINUS factor
#              | LPAREN expression RPAREN
#
# -----------------------------------------------------------------------------

# e => H
# e => O
# H => HO
# H => OH
# O => HH

from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = ( 'H', 'O', 'HE', )

# Ignored characters
t_ignore = '\n'

t_H = r'H,'
t_O = r'O,'
t_HE = r'He,'

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()

# --- Parser

# e => H
# e => O
def p_e1(p):
    '''
    e_molecule : h
    '''
    p[0] = ('z', p[1],)

def p_e2(p):
    '''
    e_molecule : o
    '''
    p[0] = ('z', p[1],)

# H => HO
# H => OH
# [H => H]?

def p_h0(p):
    '''
    h : H
    '''
    p[0] = (p[1],)
    # p[0] = ('H-foo',)

def p_h1(p):
    '''
    h : h o
    '''
    p[0] = ('z', p[1], p[2])

def p_h2(p):
    '''
    h : o h
    '''
    p[0] = ('z', p[1], p[2])

# O => HH
# [O => O]?

def p_o0(p):
    '''
    o : O
    '''
    p[0] = (p[1],)
    # p[0] = ('O-foo',)

def p_o1(p):
    '''
    o : h h h
    '''
    p[0] = ('z', p[1], p[2], p[3])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

if __name__ == '__main__':
    # Build the parser
    parser = yacc()

    # Parse an expression
    ast = parser.parse('H,H,H,')
    print(ast)
