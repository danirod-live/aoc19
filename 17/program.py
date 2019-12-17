import sys
from intcode import Computer

def read_camera_output(computer):
    output = ""
    while not computer.halted:
        computer.step()
        if computer.stdout:
            output += "".join([chr(s) for s in computer.stdout])
            computer.stdout = []
    return output

def scaffolds(cam):
    outputs = set()
    rows = cam.split("\n")
    for y in range(len(rows)):
        row = rows[y]
        for x in range(len(row)):
            if rows[y][x] == '#':
                outputs.add((x, y))
    return outputs

def neirghbours(point):
    x, y = point
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

def map_neirghbours(scaffolds):
    def count_neirghbours(p):
        return len([p for p in neirghbours(p) if p in scaffolds])
    return {p:count_neirghbours(p) for p in scaffolds}

sample = """..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^.."""

code = [int(x) for x in open("input.txt").readline().split(",")]
computer = Computer(code)
output = read_camera_output(computer)
scafs = scaffolds(output)
neirgh = map_neirghbours(scafs)

intersections = [p for p,c in neirgh.items() if c > 2]

p1 = sum([x*y for x,y in intersections])
# print(p1)

code = [int(x) for x in open("input.txt").readline().split(",")]
computer = Computer(code)
computer.program[0] = 2
computer.stdin += [ord(x) for x in
                   "A,C,C,A,B,A,B,A,B,C\nR,6,R,6,R,8,L,10,L,4\nL,4,L,12,R,6,L,10\nR,6,L,10,R,8\nn\n"]
computer.simulate()
spacemap = "".join([chr(x) for x in computer.stdout])
# spacemap = spacemap.split("Continuous video feed?")[1]
print(spacemap)

print(computer.stdout[-1])
