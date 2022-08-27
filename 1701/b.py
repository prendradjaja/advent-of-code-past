def main():
    text = open('in').read().strip()
    answer = captcha(text)
    print(answer)


def captcha(s):
    result = 0
    for i, a in enumerate(s):
        b = s[(i + len(s) // 2) % len(s)]
        if a == b:
            result += int(a)
    return result


if __name__ == '__main__':
    main()
