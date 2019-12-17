import sys

class InfiniteList(list):

    def __getitem__(self, i):
        if isinstance(i, int) and len(self) <= i:
            missing = i - len(self) + 1
            self.extend([0 for i in range(missing)])
        return list.__getitem__(self, i)

    def __setitem__(self, i, val):
        if isinstance(i, int) and len(self) <= i:
            missing = i - len(self) + 1
            self.extend([0 for i in range(missing)])
        return list.__setitem__(self, i, val)


class Computer:
    OPCODE_SIZES = {
        1: 4,
        2: 4,
        3: 2,
        4: 2,
        5: 3,
        6: 3,
        7: 4,
        8: 4,
        9: 2,
        99: 0,
    }

    def __init__(self, code, debug=False):
        self.program = InfiniteList([i for i in code])
        self.pc = 0
        self.rb = 0 # relative base
        self.stdin = []
        self.stdout = []
        self.debug = debug
        self.last_opcode = 0

    def log(self):
        opcode, mode1, mode2, mode3 = self.__opcode()
        arg_count = self.OPCODE_SIZES[opcode] - 1

        arguments, values = [], []
        if arg_count >= 1:
            arguments.append(self.program[self.pc + 1])
            values.append(self.__operand(1, mode1))
        if arg_count >= 2:
            arguments.append(self.program[self.pc + 2])
            values.append(self.__operand(2, mode2))
        if arg_count >= 3:
            arguments.append(self.program[self.pc + 3])
            values.append(self.__operand(3, mode3))

        context = {
            "pc": self.pc,
            "rb": self.rb,
            "stdin": self.stdin,
            "stdout": self.stdout,
            "opcode": self.program[self.pc],
            "opdecode": self.__opcode(),
            "arguments": arguments[0:arg_count],
            "values": values[0:arg_count],
        }
        print(context)

    def step(self):
        opcode, mode1, mode2, mode3 = self.__opcode()
        branched = False

        if self.debug:
            self.log()

        if opcode == 1:
            par1 = self.__operand(1, mode1)
            par2 = self.__operand(2, mode2)
            par3 = self.__operand(3, 1)
            if mode3 == 2:
                par3 += self.rb
            self.program[par3] = par1 + par2
        elif opcode == 2:
            par1 = self.__operand(1, mode1)
            par2 = self.__operand(2, mode2)
            par3 = self.__operand(3, 1)
            if mode3 == 2:
                par3 += self.rb
            self.program[par3] = par1 * par2
        elif opcode == 3:
            value = self.stdin[0]
            self.stdin = self.stdin[1:]
            par1 = self.__operand(1, 1)
            if mode1 == 2:
                par1 += self.rb
            self.program[par1] = value
        elif opcode == 4:
            par1 = self.__operand(1, mode1)
            self.stdout.append(par1)
        elif opcode == 5:
            par1 = self.__operand(1, mode1)
            par2 = self.__operand(2, mode2)
            if par1 != 0:
                self.pc = par2
                branched = True
        elif opcode == 6:
            par1 = self.__operand(1, mode1)
            par2 = self.__operand(2, mode2)
            if par1 == 0:
                self.pc = par2
                branched = True
        elif opcode == 7:
            par1 = self.__operand(1, mode1)
            par2 = self.__operand(2, mode2)
            par3 = self.__operand(3, 1)
            if mode3 == 2:
                par3 += self.rb
            self.program[par3] = 1 if par1 < par2 else 0
        elif opcode == 8:
            par1 = self.__operand(1, mode1)
            par2 = self.__operand(2, mode2)
            par3 = self.__operand(3, 1)
            if mode3 == 2:
                par3 += self.rb
            self.program[par3] = 1 if par1 == par2 else 0
        elif opcode == 9:
            par1 = self.__operand(1, mode1)
            self.rb += par1

        self.last_opcode = opcode
        if not branched:
            self.pc += self.OPCODE_SIZES[opcode]

    def simulate(self):
        while not self.halted:
            self.step()

    def __opcode(self):
        full_opcode = self.program[self.pc]
        opcode = full_opcode % 100
        mode_par1 = int(full_opcode / 100) % 10
        mode_par2 = int(full_opcode / 1000) % 10
        mode_par3 = int(full_opcode / 10000) % 10
        return (opcode, mode_par1, mode_par2, mode_par3)

    def __operand(self, i, mode):
        operand = self.program[self.pc + i]
        if mode == 0:
            operand = self.program[operand]
        elif mode == 2:
            operand = self.program[self.rb + operand]
        return operand

    @property
    def halted(self):
        return self.last_opcode == 99

if __name__ == "__main__":
    code = [int(x) for x in open("input.txt").readline().split(",")]
    computer = Computer(code)
    while not computer.halted:
        computer.step()
        if computer.stdout:
            sys.stdout.write("".join([str(s) for s in computer.stdout]))
            computer.stdout = []

