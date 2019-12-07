import itertools
import sys
from intcode import Computer

input_prg = [int(x) for x in open("input.txt").readline().split(",")]

def acs(phase_sequence):
    next_stdin = 0
    for next_phase in phase_sequence:
        computer = Computer(input_prg, debug=False)
        computer.stdin.append(next_phase)
        computer.stdin.append(next_stdin)
        computer.simulate()
        next_stdin = computer.stdout.pop()
    return next_stdin

def acs_2(phase_sequence):
    computers = []
    for next_phase in phase_sequence:
        computer = Computer(input_prg)
        computer.stdin.append(next_phase)
        computers.append(computer)

    computer, next_computer = 0, 1
    computers[computer].stdin.append(0)
    last_output = 0
    while True:
        while not computers[computer].stdout:
            computers[computer].step()
            if computers[computer].halted:
                return last_output
        last_output = computers[computer].stdout.pop()
        computers[next_computer].stdin.append(last_output)
        computer, next_computer = next_computer, (next_computer + 1) % 5

permutations = itertools.permutations([0, 1, 2, 3, 4])
values = [acs(perm) for perm in permutations]
answer1 = max(values)

permutations = itertools.permutations([5, 6, 7, 8, 9])
values = [acs_2(perm) for perm in permutations]
answer2 = max(values)

print({"answer1": answer1, "answer2": answer2})
