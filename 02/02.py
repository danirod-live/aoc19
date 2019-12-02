import sys

def init(noun, verb):
    # Load the program into memory
    input_prg = [int(x) for x in open("input.txt").readline().split(",")]

    # Load the 1202 Module
    input_prg[1] = noun
    input_prg[2] = verb

    # Init the computer
    return {
        "program": input_prg,
        "pc": 0,
    }

def simulate(m):
    opcode = m["program"][m["pc"]]

    # Leave
    if opcode == 99:
        return

    # Get the pointers where the input and output is
    ptr_input1 = m["program"][m["pc"] + 1]
    ptr_input2 = m["program"][m["pc"] + 2]
    ptr_output = m["program"][m["pc"] + 3]

    # Get the actual values.
    input1 = m["program"][ptr_input1]
    input2 = m["program"][ptr_input2]

    if opcode == 1:
        output = input1 + input2
    elif opcode == 2:
        output = input1 * input2
    m["program"][ptr_output] = output
    m["pc"] += 4
    simulate(m)

def result(noun, verb):
    computer = init(noun, verb)
    simulate(computer)
    return computer["program"][0]

for noun in range(99):
    for verb in range(99):
        computer = init(noun, verb)
        simulate(computer)
        output = computer["program"][0]
        print((noun, verb, output, 100 * noun + verb))
        if output == 19690720:
            sys.exit(0)
