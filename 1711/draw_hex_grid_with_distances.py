from gridlib import gridsource as gridlib
from b import distance_from_origin, DIRECTIONS


R_SCALE = 1
C_SCALE = 4


image = {}
for norths in range(-4, 4+1):
    for northeasts in range(-4, 4+1):
        position = gridlib.addvec(
            gridlib.mulvec(DIRECTIONS['n'], norths),
            gridlib.mulvec(DIRECTIONS['ne'], northeasts),
        )
        r, c = position
        image[(r * R_SCALE, c * C_SCALE)] = str(distance_from_origin(position))[:1]
image[(0, 0)] = '*'


rmin = min(pos[0] for pos in image)
rmax = max(pos[0] for pos in image)
cmin = min(pos[1] for pos in image)
cmax = max(pos[1] for pos in image)

for r in range(rmin, rmax+1):
    for c in range(cmin, cmax+1):
        ch = image.get((r, c), ' ')
        print(ch, end='')
    print()
