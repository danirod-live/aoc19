from intcode import InfiniteList

def test_infinite_list_behaves_like_list():
    lst = InfiniteList([1, 2, 3, 4])
    assert len(lst) == 4
    assert lst[0] == 1
    assert lst[1] == 2
    assert lst[2] == 3
    assert lst[3] == 4
    assert lst[0:4] == [1, 2, 3, 4]

def test_infinite_list_gets_values_at_random_positions():
    lst = InfiniteList([1, 2, 3, 4])
    value = lst[5]
    assert value == 0
    assert len(lst) == 6
    assert lst[4:6] == [0, 0]

def test_infinite_list_sets_values_at_random_positins():
    lst = InfiniteList([1, 2, 3, 4])
    lst[5] = 6
    assert len(lst) == 6
    assert lst == [1, 2, 3, 4, 0, 6]
