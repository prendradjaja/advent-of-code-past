def main():
    text = open('in').read().strip()
    answer = captcha(text)
    print(answer)


def captcha(s):
    result = 0
    for a, b in zip(s, s[1:] + s[:1]):
        if a == b:
            result += int(a)
    return result


if __name__ == '__main__':
    main()
