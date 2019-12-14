from intcode import Computer
from curses import wrapper
import curses

TILES = {
    0: ' ',
    1: '#',
    2: 'x',
    3: '-',
    4: '·',
}

ball_x, pad_x = 0, 0

def main(stdscr):
    code = [int(x) for x in open("input.txt").readline().split(",")]
    computer = Computer(code)
    computer.program[0] = 2

    stdscr.clear()
    stdscr.nodelay(True)
    while not computer.halted:
        try:
            computer.step()
        except IndexError:
            if pad_x > ball_x:
                computer.stdin.append(-1)
            elif pad_x < ball_x:
                computer.stdin.append(1)
            else:
                computer.stdin.append(0)
            computer.step()
            curses.napms(1)
        if len(computer.stdout) == 3:
            x, y, tileID = computer.stdout[0:3]
            computer.stdout = computer.stdout[3:]
            if x == -1:
                stdscr.addstr(0, 10, str(tileID))
            else:
                stdscr.addch(y+2, x, TILES[tileID])
                if tileID == 3:
                    pad_x = x
                elif tileID == 4:
                    ball_x = x
            stdscr.refresh()
    stdscr.nodelay(False)
    curses.napms(1000)

wrapper(main)
