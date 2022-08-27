import re


def main():
    print('''
import Data.Bits ((.&.), (.|.), shift)
import qualified Data.Bits (complement)


main = print a'

rshift a b = shift a (-b)

complement :: Int -> Int
complement = Data.Bits.complement
    '''.strip() + '\n')

    for line in open('in').read().strip().splitlines():
        line = add_ticks(line)
        expr, dest = line.split(' -> ')
        expr = (
            expr
                .replace('NOT', 'complement')
                .replace('AND', '.&.')
                .replace('OR', '.|.')
                .replace('LSHIFT', '`shift`')
                .replace('RSHIFT', '`rshift`')
        )
        line = f'{dest} = {expr}'
        print(line)


def add_ticks(expr):
    '''
    Add a tick to the end of every variable name (to avoid collisions with
    reserved words)

    >>> add_ticks("a bc def")
    "a' bc' def'"
    '''
    return re.sub(
        r'[a-z]\b',
        "\g<0>'",
        expr
    )


main()
