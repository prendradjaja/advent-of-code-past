def main():
    answer = 0
    for password in range(158126, 624574+1):
        digits = [int(digit) for digit in str(password)]
        if nondecreasing(digits) and has_pair(digits):
            answer += 1
    print(answer)


def nondecreasing(lst):
    return lst == sorted(lst)


def has_pair(lst):
    for a, b in zip(lst, lst[1:]):
        if a == b:
            return True
    return False


main()
