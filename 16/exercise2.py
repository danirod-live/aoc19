from itertools import islice

def fft(invalue):
    instr = [int(x) for x in invalue]
    instr.reverse()
    output = []
    for i in range(len(invalue)):
        if i == 0:
            output.append(instr[0])
        else:
            output.append((instr[i] + output[i-1]) % 10)
    output.reverse()
    return "".join([str(x) for x in output])

def fft_m(invalue, count):
    acc = invalue
    for i in range(count):
        print(i, count)
        acc = fft(acc)
    return acc

invalue = open("input.txt").readline().strip()
invalue = invalue * 10000
offset = int(invalue[0:7])
substring = invalue[offset:]
print(fft_m(substring, 100))
