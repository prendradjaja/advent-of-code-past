def main():
    answer = 0
    for line in open('in').read().splitlines():
        l, w, h = [int(n) for n in line.split('x')]
        answer += paper_needed(l, w, h)
    print(answer)


def paper_needed(l, w, h):
    return surface_area(l, w, h) + min(l * w, w * h, l * h)


def surface_area(l, w, h):
    return 2*l*w + 2*w*h + 2*h*l


main()
