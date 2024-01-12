'''
Usage:

    python3 generate_grammar.py input.txt > parser.py
    python3 parser.py
    # And then count the number of z's in the output -- that's the answer
'''

import sys
import re
import itertools

def bprint(s):  # "Block print"
    assert s[0] == '\n'
    assert s[-1] == '\n'
    print(s[1:-1])

def parse_molecule(molecule):
    return tuple(
        re.sub(r'[A-Z]', r' \g<0>', molecule)  # Add a space before every capital letter
        .split()
    )

def parse_rules(rules):
    result = []
    for line in rules.splitlines():
        left, right = line.split(' => ')
        right = parse_molecule(right)
        result.append((left, right))
    return result

def preprocess_molecule(molecule):
    '''
    >>> preprocess_molecule('e')
    'e,'
    >>> preprocess_molecule('HeH')
    'He,H,'
    >>> preprocess_molecule('HOH')
    'H,O,H,'
    '''
    result = ''
    for each in (
        re.sub(r'[A-Z]', r' \g<0>', molecule)  # Add a space before every capital letter
        .split()
    ):
        result += each + ','
    return result

path = sys.argv[1]
text = open(path).read()
rules, molecule = text.split('\n\n')
rules = sorted(parse_rules(rules))
molecule = preprocess_molecule(molecule)
rules_grouped = [(k, list(g)) for k, g in itertools.groupby(rules, lambda x: x[0])]
rules_grouped.sort(key=lambda s: s[0].swapcase())  # Move e rules to the start

lefts = [left for left, right in rules]
elements = tuple(sorted(
    (set(lefts) | {atom for left, right in rules for atom in right}) - {'e'}
))
capitalized_elements = tuple(e.upper() for e in elements)
inert_elements = [each for each in elements if each not in lefts]

bprint(
fr'''
from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = {repr(capitalized_elements)}

# Ignored characters
t_ignore = '\n'

''')

for each in elements:
    print(f"t_{each.upper()} = r'{each},'")

bprint(
fr'''

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {{t.value[0]!r}}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()

# --- Parser

''')

for group_name, group in rules_grouped:
    print(f'# {group_name}')
    if group_name != 'e':
        bprint(f"""
def p_{group_name.lower()}0(p):
    '''
    {group_name.lower()} : {group_name.upper()}
    '''
    p[0] = (p[1],)

""")
    for i, (left, right) in enumerate(group, start=1):
        # print(right, i)
        assert left == group_name
        right_str = ' '.join(each.lower() for each in right)
        parse_result = "('z'"
        for j, each in enumerate(right, start=1):
            parse_result += f', p[{j}]'
        parse_result += ')'
        bprint(
f"""
def p_{group_name.lower()}{i}(p):
    '''
    {group_name.lower()} : {right_str}
    '''
    p[0] = {parse_result}

""")

for group_name in sorted(inert_elements):
    bprint(f"""
def p_{group_name.lower()}0(p):
    '''
    {group_name.lower()} : {group_name.upper()}
    '''
    p[0] = (p[1],)

""")

bprint(
f'''

def p_error(p):
    print(f'Syntax error at {{p.value!r}}')

if __name__ == '__main__':
    # Build the parser
    parser = yacc()

    # Parse an expression
    ast = parser.parse({repr(molecule)})
    print(ast)
''')
