from sandbox_ply import lexer

import re
import fileinput


# def preprocess_molecule(molecule):
#     '''
#     >>> preprocess_molecule('e')
#     'e,'
#     >>> preprocess_molecule('HeH')
#     'He,H,'
#     >>> preprocess_molecule('HOH')
#     'H,O,H,'
#     '''
#     result = ''
#     for each in (
#         re.sub(r'[A-Z]', r' \g<0>', molecule)  # Add a space before every capital letter
#         .split()
#     ):
#         result += each + ','
#     return result


if __name__ == '__main__':
    molecule_string = 'H,O,H,'

    lexer.input(molecule_string)

    for tok in lexer:
        print('{}\t{}'.format(tok.value, tok.type))
