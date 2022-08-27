from a import spiral


window_size = 4
spiral_size = 3

image = {}
for i, pos in enumerate(spiral(spiral_size), start=1):
    image[pos] = i

for r in range(-window_size, window_size+1):
    for c in range(-window_size, window_size+1):
        pos = r, c
        if pos in image:
            print(image[pos], end='\t')
        else:
            print('.', end='\t')
    print()
