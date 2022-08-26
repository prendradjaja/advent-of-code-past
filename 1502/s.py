def main():
    answer = 0
    for line in open('in').read().splitlines():
        l, w, h = [int(n) for n in line.split('x')]
        answer += ribbon_needed(l, w, h)
    print(answer)


def ribbon_needed(l, w, h):
    shortest_distance_around = min(
        perimeter(l, w),
        perimeter(w, h),
        perimeter(l, h)
    )
    return shortest_distance_around + volume(l, w, h)


def perimeter(a, b):
    return 2*a + 2*b


def volume(l, w, h):
    return l * w * h


main()
