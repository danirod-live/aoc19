from problem import Image

sample_input = "0222112222120000"

def test_layer_count():
    img = Image(sample_input, 2, 2)
    assert len(img.layers) == 4

def test_layer_count_2():
    img = Image("123456789012", 3, 2)
    assert len(img.layers) == 2

def test_split_layers():
    img = Image(sample_input, 2, 2)
    assert img.layers[0] == "0222"
    assert img.layers[1] == "1122"
    assert img.layers[2] == "2212"
    assert img.layers[3] == "0000"

def test_split_layers_2():
    img = Image("123456789012", 3, 2)
    assert img.layers[0] == "123456"
    assert img.layers[1] == "789012"

def test_pixelat():
    img = Image(sample_input, 2, 2)
    assert img.pixelat(0) == "0"
    assert img.pixelat(1) == "1"
    assert img.pixelat(2) == "1"
    assert img.pixelat(3) == "0"

def test_compose():
    img = Image(sample_input, 2, 2)
    assert img.compose() == "0110"
