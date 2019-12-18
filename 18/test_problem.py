from problem import available_keys, position

CASE_1 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

def test_position():
    assert position(CASE_1, "@") == (15, 1)
    assert position(CASE_1, "a") == (17, 1)
    assert position(CASE_1, "f") == (1, 1)
    assert position(CASE_1, "d") == (1, 3)

def test_available_keys_empty():
    position = (15, 1)
    keys = []
    outputs = available_keys(CASE_1, position, keys)
    assert len(outputs) == 1
    assert outputs[0] == ('a', 2)

def test_available_keys_with_key():
    position = (17, 1)
    keys = ['a']
    outputs = available_keys(CASE_1, position, keys)
    assert len(outputs) == 1
    assert outputs[0] == ('b', 6)

def test_available_keys_when_multiple_options():
    position = (21, 1)
    keys = ['a', 'b', 'c']
    outputs = available_keys(CASE_1, position, keys)
    assert len(outputs) == 2
    candidates = [k for k,d in outputs]
    assert 'd' in candidates
    assert 'e' in candidates

def test_available_keys_when_no_more_candidates():
    position = (1, 1)
    keys = ['a', 'b', 'c', 'd', 'e', 'f']
    outputs = available_keys(CASE_1, position, keys)
    assert len(outputs) == 0
