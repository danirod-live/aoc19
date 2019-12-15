from intcode import Computer
from collections import defaultdict

code = [int(x) for x in open("input.txt").readline().split(",")]

NOT_KNOWN = 0
WALL = 1
AIR = 2
OXYGEN = 3

TILES = {
    NOT_KNOWN: " ",
    WALL: "#",
    AIR: ".",
    OXYGEN: "o",
}

def print_map(board):
    min_y = min(board.keys())
    min_x = min([min(row.keys()) for row in board.values()])
    max_y = max(board.keys())
    max_x = max([max(row.keys()) for row in board.values()])
    print("".join(["-" for i in range(min_x, max_x + 3)]) + " " + str(min_y))
    for y in range(min_y, max_y + 1):
        row = [TILES[board[y][x]] for x in range(min_x, max_x + 1)]
        print("|" + "".join(row) + "|")
    print("".join(["-" for i in range(min_x, max_x + 3)]) + " " + str(max_y))
    print(str(min_x) + "".join([" " for i in range(min_x, max_x + 3)]) + " " + str(max_x))


def row_builder():
    return defaultdict(int)
def map_builder():
    return defaultdict(row_builder)

def state():
    return {
        "map": map_builder(),
        "pos": (0, 0),
        "computer": Computer(code),
		"oxygen": None,
    }

def move(problem, direction):
    # Move to the next spot
    problem["computer"].stdin.append(direction)
    while not problem["computer"].halted and not problem["computer"].stdout:
        problem["computer"].step()
    output = problem["computer"].stdout[0]
    problem["computer"].stdout = problem["computer"].stdout[1:]

    # Get the target coordinates we want to move to.
    x, y = problem["pos"]
    if direction == 1:
        target = (x, y - 1)
    elif direction == 2:
        target = (x, y + 1)
    elif direction == 3:
        target = (x - 1, y)
    elif direction == 4:
        target = (x + 1, y)

    # We can only move if there isn't any wall.
    if output != 0:
        problem["pos"] = target

    # Update the map
    tx, ty = target
    if output == 0:
        problem["map"][ty][tx] = WALL
    if output == 1:
        problem["map"][ty][tx] = AIR
    if output == 2:
        problem["oxygen"] = (tx, ty)
        problem["map"][ty][tx] = OXYGEN

    return output

def min_distance(problem, visited=None):
    if not visited:
        visited = set()
    visited.add(problem["pos"])
    distances = []


    # Try north
    north = move(problem, 1)
    if north == 1 or north == 2:
        if not problem["pos"] in visited:
            if north == 2:
                distances.append(1)
            elif north == 1:
                dist = min_distance(problem, visited)
                if dist:
                    distances.append(dist + 1)
        move(problem, 2) # undo

    # Try south
    south = move(problem, 2)
    if south == 1 or south == 2:
        if not problem["pos"] in visited:
            if south == 2:
                distances.append(1)
            elif south == 1:
                dist = min_distance(problem, visited)
                if dist:
                    distances.append(dist + 1)
        move(problem, 1)

    # Try west
    west = move(problem, 3)
    if west == 1 or west == 2:
        if not problem["pos"] in visited:
            if west == 2:
                distances.append(1)
            elif west == 1:
                dist = min_distance(problem, visited)
                if dist:
                    distances.append(dist + 1)
        move(problem, 4)

    # Try east
    east = move(problem, 4)
    if east == 1 or east == 2:
        if not problem["pos"] in visited:
            if east == 2:
                distances.append(1)
            elif east == 1:
                dist = min_distance(problem, visited)
                if dist:
                    distances.append(dist + 1)
        move(problem, 3)

    visited.remove(problem["pos"])
    if not distances:
        return None
    return min(distances)

def points_to_oxygenate_next(map, position):
    x, y = position
    surrounds = [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]
    return [s for s in surrounds if map[s[1]][s[0]] == AIR]

def fill_step(map, bounds):
    next_bounds = []
    for bound in bounds:
        next_bounds += points_to_oxygenate_next(map, bound)
    for next_bound in next_bounds:
        map[next_bound[1]][next_bound[0]] = OXYGEN
    return next_bounds

problem = state()
print(min_distance(problem))
print_map(problem["map"])
bounds = (problem["oxygen"],)
step = 0
while len(bounds) > 0:
    bounds = fill_step(problem["map"], bounds)
    step += 1
    print_map(problem["map"])
print(step)
