import sys
from util import ints
from string import ascii_lowercase


def main():
    f = open('in')
    starting_order = ascii_lowercase[:16]
    programs = list(starting_order)

    dance = f.read().split(',')

    print('''
Simulating 1 billion dances would take too long. So we need a trick:

It turns out that the programs return to their starting order after 42 dances
-- so we only need to simulate 42 dances to find the answer!

  Aside:

  This is in no way obvious from the problem description! There are 16
  factorial -- approx. 21 trillion -- possible permutations, so the cycle
  could be prohibitively long. Actually, some smart people have found an
  upper bound much smaller than 21 trillion -- but this is getting even deeper
  into "not obvious" territory.

  https://www.reddit.com/r/adventofcode/comments/7k5mrq/comment/drbraxn/
'''.strip())
    print()

    print('n', 'Order after n dances', sep='\t')
    print('-', '--------------------', sep='\t')

    print(0, ''.join(programs), sep='\t')

    dots_printed = False
    for k in range(1, 42+1):
        for move in dance:
            move = move.strip()
            if move[0] == 's':
                n = int(move[1:])
                programs = programs[-n:] + programs[:-n]
            elif move[0] == 'x':
                left, right = ints(move[1:].split('/'))
                programs[left], programs[right] = programs[right], programs[left]
            elif move[0] == 'p':
                left, right = move[1:].split('/')
                i = programs.index(left)
                j = programs.index(right)
                programs[i], programs[j] = programs[j], programs[i]
            else:
                1/0

        if k < 4 or k > 30:
            print(k, ''.join(programs), sep='\t')
            if k == 34:
                answer = ''.join(programs)
        elif not dots_printed:
            print('...')
            dots_printed = True

    assert ''.join(programs) == starting_order

    print()
    print('''
Therefore, the order after 1 billion dances is the same as the order after 1
billion mod 42 dances. 1 billion mod 42 is 34, so the answer is:
    '''.strip())
    print()

    print(answer)


# Some incomplete code from going down what I thought was the wrong road -- in
# case I ever want to try doing this again via exponentiation by squaring. Key
# insight:
#
#     You can decompose the underlying transformation here into partner swaps
#     and non-partner swaps. So the overall transformation T is given by
#     applying the non-partner swaps, then applying all the partner swaps. The
#     critical thing to notice here is that the non-partner swaps form a
#     permutation of the string - call this permutation X. The partner swaps,
#     however, form a permutation of the indices on the characters in the
#     string (that is, imagine the string indexing into a dictionary
#     containing 0 -> 15 and swapping the values in the dictionary, then at
#     the end re-ordering the string by those values). Call this permutation
#     P. You can apply X and P in any order, and if you want to apply T an
#     arbitrary number of times, you can compute X that number of times and
#     then P that number of times and get the same result as if you'd
#     interleaved them.
#
#     https://www.reddit.com/r/adventofcode/comments/7k5mrq/comment/drbraxn/

# def permutation_to_matrix(permutation):
#     assert len(permutation) <= len(ascii_lowercase)
#     n = len(permutation)
#
#     matrix = []
#     for _ in range(n):
#         matrix.append([0] * n)
#
#     for i, ch in enumerate(permutation):
#         row = ascii_lowercase.index(ch)
#         col = i
#         matrix[row][col] = 1
#
#     # for row in matrix:
#     #     print(row)
#
#     return matrix
#
# def matmul(a,b):
#     '''
#     >>> A = [[1, 2, 3]]
#     >>> B = [[4], [5], [6]]
#     >>> matmul(A, B)
#     [[32]]
#     >>> BA_expected = [
#     ...     [4, 8, 12],
#     ...     [5, 10, 15],
#     ...     [6, 12, 18],
#     ... ]
#     >>> matmul(B, A) == BA_expected
#     True
#     Copied from https://stackoverflow.com/a/48597323/1945088
#     '''
#     c = []
#     for i in range(0,len(a)):
#         temp=[]
#         for j in range(0,len(b[0])):
#             s = 0
#             for k in range(0,len(a[0])):
#                 s += a[i][k]*b[k][j]
#             temp.append(s)
#         c.append(temp)
#     return c
#
# original_string = 'abcde'
# permutation_matrix = permutation_to_matrix('baedc')
# n = len(original_string)
#
# # To indices
# vector = [list(range(n))]
#
# # Transform
# for _ in range(2):
#     vector = matmul(vector, permutation_matrix)
#
# # From indices
# indices = vector[0]
# print(''.join(ascii_lowercase[idx] for idx in indices))


if __name__ == '__main__':
    main()
