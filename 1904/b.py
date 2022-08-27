def main():
    answer = 0
    for password in range(158126, 624574+1):
        digits = [int(digit) for digit in str(password)]
        if nondecreasing(digits) and has_isolated_pair(digits):
            answer += 1
    print(answer)


def nondecreasing(lst):
    return lst == sorted(lst)


def has_isolated_pair(lst):
    lst = [None] + lst + [None]
    for z, a, b, c in zip(lst, lst[1:], lst[2:], lst[3:]):
        if z != a == b != c:
            return True
    return False


main()
