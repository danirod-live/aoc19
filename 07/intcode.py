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
        99: 0,
    }

    ALWAYS_DIRECT = {
        1: [3],
        2: [],
        3: [1, 2, 7, 8],
    }

    def __init__(self, code, debug=False):
        self.program = [i for i in code]
        self.pc = 0
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
            "code": self.program,
            "pc": self.pc,
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
            par3 = self.__operand(3, mode3)
            self.program[par3] = par1 + par2
        elif opcode == 2:
            par1 = self.__operand(1, mode1)
            par2 = self.__operand(2, mode2)
            par3 = self.__operand(3, mode3)
            self.program[par3] = par1 * par2
        elif opcode == 3:
            value = self.stdin[0]
            self.stdin = self.stdin[1:]
            par1 = self.__operand(1, mode1)
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
            par3 = self.__operand(3, mode3)
            self.program[par3] = 1 if par1 < par2 else 0
        elif opcode == 8:
            par1 = self.__operand(1, mode1)
            par2 = self.__operand(2, mode2)
            par3 = self.__operand(3, mode3)
            self.program[par3] = 1 if par1 == par2 else 0

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

        # Some opcodes only use direct style.
        if opcode in self.ALWAYS_DIRECT[1]:
            mode_par1 = 1
        if opcode in self.ALWAYS_DIRECT[2]:
            mode_par2 = 1
        if opcode in self.ALWAYS_DIRECT[3]:
            mode_par3 = 1

        return (opcode, mode_par1, mode_par2, mode_par3)

    def __operand(self, i, mode):
        operand = self.program[self.pc + i]
        if mode == 0:
            operand = self.program[operand]
        return operand

    @property
    def halted(self):
        return self.last_opcode == 99

