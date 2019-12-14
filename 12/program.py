import math

positions = [
    # (-8, -10, 0),
    # (5, 5, 10),
    # (2, -7, 3),
    # (9, -8, -3),
    # (-1, 0, 2),
    # (2, -10, -7),
    # (4, -8, 8),
    # (3, 5, -1),
    [4, 12, 13],
    [-9, 14, -3],
    [-7, -1, 2],
    [-11, 17, -1],
]

speeds = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

problem = {
    "positions": positions,
    "speeds": speeds,
    "timestep": 0,
}

def reset(problem):
    problem["positions"] = [
        [4, 12, 13],
        [-9, 14, -3],
        [-7, -1, 2],
        [-11, 17, -1],
    ]
    problem["speeds"] = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    problem["timestep"] = 0

def tick_c(problem, c):
    for i in range(4):
        for j in range(4):
            pi = problem["positions"][i][c]
            pj = problem["positions"][j][c]
            if pi > pj:
                problem["speeds"][i][c] -= 1
            elif pi < pj:
                problem["speeds"][i][c] += 1
    for i in range(4):
        problem["positions"][i][c] += problem["speeds"][i][c]

def tick(problem):
    for c in range(3):
        tick_c(problem, c)
    problem["timestep"] += 1

def module(vector):
    x, y, z = vector
    return abs(x) + abs(y) + abs(z)

for i in range(1000):
    tick(problem)

p1 = sum([
    module(problem["positions"][i]) * module(problem["speeds"][i])
    for i in range(4)
])
print(p1)

reset(problem)
x0 = [c[0] for c in problem["positions"]]
y0 = [c[1] for c in problem["positions"]]
z0 = [c[2] for c in problem["positions"]]

def lcm(a, b):
    return (a * b) // math.gcd(a, b)

def find(compo, initial):
    problem = {}
    reset(problem)
    i = 0
    while True:
        tick_c(problem, compo)
        i += 1
        val = [c[compo] for c in problem["positions"]]
        speed = [c[compo] for c in problem["speeds"]]
        if val == initial and speed == [0, 0, 0, 0]:
            return i

x = find(0, x0)
y = find(1, y0)
z = find(2, z0)
print(lcm(lcm(x, y), z))
