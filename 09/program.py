from intcode import Computer

prg = [int(x) for x in open("input.txt").readline().split(",")]

computer = Computer(prg, debug=False)
computer.stdin.append(2)
computer.simulate()
print(computer.stdout)
