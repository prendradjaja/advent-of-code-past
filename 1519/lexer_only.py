from sandbox_ply import lexer

import fileinput


file = ''
for line in fileinput.input():
    file += line

lexer.input(file)

for tok in lexer:
    print('{}\t{}'.format(tok.value, tok.type))
