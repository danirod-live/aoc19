import sys
from intcode import Computer
from collections import defaultdict

code = [int(x) for x in open("input.txt").readline().split(",")]

def row_factory():
    return defaultdict(int)
def panel_factory():
    return defaultdict(row_factory)

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

def move(px, py, side):
    if side == UP:
        py -= 1
    elif side == DOWN:
        py += 1
    elif side == LEFT:
        px -= 1
    elif side == RIGHT:
        px += 1
    return px, py

def paint(panel):
    painted = set()
    px, py = 0, 0
    side = UP
    computer = Computer(code, debug=False)
    computer.stdin.append(panel[py][px])
    while not computer.halted:
        computer.step()
        if len(computer.stdout) == 2:
            color_to_paint, direction_to_move = computer.stdout
            computer.stdout = []
            panel[py][px] = color_to_paint
            painted.add((px, py))
            if direction_to_move == 0:
                side = (side - 1) % 4
            elif direction_to_move == 1:
                side = (side + 1) % 4
            px, py = move(px, py, side)
            computer.stdin.append(panel[py][px])
    return painted

def print_panel(panel):
    min_y = min(panel.keys())
    min_x = min([min(row.keys()) for row in panel.values()])
    max_y = max(panel.keys())
    max_x = max([max(row.keys()) for row in panel.values()])
    print("".join(["-" for i in range(min_x, max_x + 3)]))
    for y in range(min_y, max_y + 1):
        row = ['#' if panel[y][x] else " " for x in range(min_x, max_x + 1)]
        print("|" + "".join(row) + "|")
    print("".join(["-" for i in range(min_x, max_x + 3)]))

panel1 = panel_factory()
p1 = len(paint(panel1))
print(p1)

panel2 = panel_factory()
panel2[0][0] = 1
painted = paint(panel2)
print_panel(panel2)
