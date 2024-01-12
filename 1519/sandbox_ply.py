from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = ('H', 'HE', 'O')

# Ignored characters
t_ignore = '\n'

t_H = r'H,'
t_HE = r'He,'
t_O = r'O,'

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()

# --- Parser

# e
def p_e1(p):
    '''
    e : h
    '''
    p[0] = ('z', p[1],)

def p_e2(p):
    '''
    e : o
    '''
    p[0] = ('z', p[1],)

# H
def p_h0(p):
    '''
    h : H
    '''
    p[0] = (p[1],)

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

# O
def p_o0(p):
    '''
    o : O
    '''
    p[0] = (p[1],)

def p_o1(p):
    '''
    o : h h
    '''
    p[0] = ('z', p[1], p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

if __name__ == '__main__':
    # Build the parser
    parser = yacc()

    # Parse an expression
    ast = parser.parse('H,H,H,')
    print(ast)
