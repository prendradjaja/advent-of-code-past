import sys

from gridlib import gridsource as gridlib
from util import Record, findints


Particle = Record('Particle', 'position velocity acceleration id')


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    particles = []
    for i, line in enumerate(lines):
        px, py, pz, vx, vy, vz, ax, ay, az = findints(line)
        particles.append(
            Particle((px, py, pz), (vx, vy, vz), (ax, ay, az), i)
        )

    # Used trial and error to determine how long to run the simulation
    for _ in range(1000):
        for p in particles:
            p.velocity = gridlib.addvec(p.velocity, p.acceleration)
            p.position = gridlib.addvec(p.position, p.velocity)

    closest_particle = min(particles, key=lambda p: gridlib.absmanhattan(p.position))
    answer = closest_particle.id
    print(answer)


if __name__ == '__main__':
    main()
