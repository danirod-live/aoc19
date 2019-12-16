from exercise_mpi import fft_n, fft

def test_simple_case():
    inval = "12345678"
    outval = "48226158"
    assert fft(inval) == outval

def test_twice():
    inval = "12345678"
    outval = "34040438"
    assert fft(fft(inval)) == outval

def test_fftn():
    inval = "12345678"
    outval = "01029498"
    assert fft_n(inval, 4) == outval

def test_complex_1():
    inval = "80871224585914546619083218645595"
    output = fft_n(inval, 100)
    assert output[0:8] == "24176176"

def test_complex_2():
    inval = "19617804207202209144916044189917"
    output = fft_n(inval, 100)
    assert output[0:8] == "73745418"

def test_complex_3():
    inval = "69317163492948606335995924319873"
    output = fft_n(inval, 100)
    assert output[0:8] == "52432133"
