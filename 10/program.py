import math
from collections import defaultdict

def read_map(file):
    lines = [x.strip() for x in open(file).readlines()]
    asteroids = []
    for nline in range(len(lines)):
        for mline in range(len(lines[nline])):
            if lines[nline][mline] == '#':
                asteroids.append((mline, nline))
    return asteroids

def vector(p, q):
    px, py = p
    qx, qy = q
    return (qx - px, qy - py)

def polares(x, y):
    dist = math.sqrt(x**2 + y**2)
    phi = math.atan2(y, x)
    while phi <= -math.pi:
        phi += math.pi
    while phi > math.pi:
        phi -= math.pi
    return dist, phi

def group_by_angle(polars):
    angles = defaultdict(list)
    for asteroid, polar in polars:
        dist, phi = polar
        angles[phi].append((dist, asteroid))
    return angles

def sight_map(amap, pivot):
    map_without_pivot = [a for a in amap if a != pivot]
    polars = [(ast, polares(*vector(pivot, ast))) for ast in map_without_pivot]
    return polars

asteroid_map = read_map("input2.txt")

# problem 1
sight_maps = [(p, sight_map(asteroid_map, p)) for p in asteroid_map]
angle_sets = [(pivot, group_by_angle(smap)) for pivot, smap in sight_maps]
visible_spots = [(p, len(a.keys())) for p, a in angle_sets]
p1 = max(visible_spots, key=lambda l: l[1])

# problem 2
pivot, _ = p1

def topositive(angle):
    while angle < 0:
        angle += 2 * math.pi
    return angle

angle_set = group_by_angle(sight_map(asteroid_map, pivot))
rotated_angle_set = {
    topositive(angle + math.pi / 2): sorted(distances, key=lambda l: l[0])
    for angle, distances in dict(angle_set).items()
}

def shoot(angle_set):
    shooting_angles = sorted(list(rotated_angle_set))
    while len(shooting_angles) > 0:
        for angle in shooting_angles:
            yield angle_set[angle][0]
            angle_set[angle] = angle_set[angle][1:]
        shooting_angles = [s for s in shooting_angles if len(angle_set[s]) > 0]

shooted_asteroids = list(shoot(rotated_angle_set))
[print(i+1, shooted_asteroids[i]) for i in range(len(shooted_asteroids))]
