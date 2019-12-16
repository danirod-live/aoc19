from itertools import islice

def pattern(pos, count):
    def genptr(pos):
        base = [0, 1, 0, -1]
        while True:
            for i in base:
                for count in range(pos):
                    yield i
    long_pattern = genptr(pos)
    return islice(long_pattern, 1, count + 1)

def fft(in_value):
    decimals = [int(s) for s in in_value]

    def process(pos):
        ptr = pattern(pos + 1, len(decimals))
        result = sum([a*b for a,b in zip(decimals, ptr)])
        return abs(result) % 10

    output = [process(i) for i in range(len(decimals))]
    return "".join([str(o) for o in output])

def fft_n(in_value, repetitions):
    acc = in_value
    for i in range(repetitions):
        acc = fft(acc)
    return acc

