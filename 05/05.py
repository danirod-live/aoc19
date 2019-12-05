import sys

def init():
    # Load the program into memory
    input_prg = [int(x) for x in open("input.txt").readline().split(",")]

    # Init the computer
    return {
        "program": input_prg,
        "pc": 0,
        "stdin": [],
    }

opcode_sizes = {
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

def simulate(m):
    full_opcode = m["program"][m["pc"]]
    opcode = full_opcode % 100
    mode_par1 = int(full_opcode / 100) % 10
    mode_par2 = int(full_opcode / 1000) % 10
    mode_par3 = int(full_opcode / 10000) % 10


    # Leave
    if opcode == 99:
        return

    # Get the parameters
    par1 = m["program"][m["pc"] + 1]
    par2 = m["program"][m["pc"] + 2]
    par3 = m["program"][m["pc"] + 3]

    dirty_pc = False

    if opcode == 1:
        if mode_par1 == 0:
            par1 = m["program"][par1]
        if mode_par2 == 0:
            par2 = m["program"][par2]
        output = par1 + par2
        m["program"][par3] = output
    elif opcode == 2:
        if mode_par1 == 0:
            par1 = m["program"][par1]
        if mode_par2 == 0:
            par2 = m["program"][par2]
        output = par1 * par2
        m["program"][par3] = output
    elif opcode == 3:
        m["program"][par1] = m["stdin"].pop()
    elif opcode == 4:
        if mode_par1 == 0:
            par1 = m["program"][par1]
        print(par1)
    elif opcode == 5:
        if mode_par1 == 0:
            par1 = m["program"][par1]
        if mode_par2 == 0:
            par2 = m["program"][par2]
        if par1 != 0:
            m["pc"] = par2
            dirty_pc = True
    elif opcode == 6:
        if mode_par1 == 0:
            par1 = m["program"][par1]
        if mode_par2 == 0:
            par2 = m["program"][par2]
        if par1 == 0:
            m["pc"] = par2
            dirty_pc = True
    elif opcode == 7:
        if mode_par1 == 0:
            par1 = m["program"][par1]
        if mode_par2 == 0:
            par2 = m["program"][par2]
        m["program"][par3] = 1 if par1 < par2 else 0
    elif opcode == 8:
        if mode_par1 == 0:
            par1 = m["program"][par1]
        if mode_par2 == 0:
            par2 = m["program"][par2]
        m["program"][par3] = 1 if par1 == par2 else 0


    if not dirty_pc:
        m["pc"] += opcode_sizes[opcode]
    simulate(m)

computer = init()
computer["stdin"].append(5)
simulate(computer)

