from collections import defaultdict

# wire1 = "R8,U5,L5,D3"
# wire2 = "U7,R6,D4,L4"
wire1, wire2, _ = open("input.txt").readlines()
# wire1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
# wire2 = "U62,R66,U55,R34,D71,R55,D58,R83"
# wire1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
# wire2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

def parse_instruction_list(wire):
    turns = wire.strip().split(",")
    return [(turn[0], int(turn[1:])) for turn in turns]

def coordinates_for_instruction(initial_coords, instruction):
    x, y = initial_coords
    direction, count = instruction
    for i in range(count):
        if direction == 'L':
            x = x - 1
        elif direction == 'R':
            x = x + 1
        elif direction == 'U':
            y = y - 1
        elif direction == 'D':
            y = y + 1
        yield (x, y)


def coordinates_for_wire(wire):
    instructions = parse_instruction_list(wire)
    current_coord = (0, 0)
    for instruction in instructions:
        coords = list(coordinates_for_instruction(current_coord, instruction))
        for cord in coords:
            yield cord
        current_coord = coords[-1]


def place_wire_in_grid(grid, wire):
    local_grid = set()
    for coordinate in coordinates_for_wire(wire):
        if coordinate in local_grid:
            continue
        local_grid.add(coordinate)
        grid[coordinate] += 1

grid = defaultdict(int)
place_wire_in_grid(grid, wire1)
place_wire_in_grid(grid, wire2)

intersections = [k for k, v in grid.items() if v > 1]
manhattans = [abs(x) + abs(y) for x, y in intersections]
closest = min(manhattans)


#### PROBLEM 2

def steps_until_point(wire, point):
    coordinates = list(coordinates_for_wire(wire))
    return coordinates.index(point) + 1

def signal_delay(wire1, wire2, point):
    return steps_until_point(wire1, point) + steps_until_point(wire2, point)

def minimum_signal_delay(wire1, wire2, intersections):
    return min([signal_delay(wire1, wire2, i) for i in intersections])

print(minimum_signal_delay(wire1, wire2, intersections))
# print(closest)

