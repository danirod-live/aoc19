from itertools import groupby

def duplicated(pw):
    groups = [list(v) for k, v in groupby(pw)]
    return 2 in [len(i) for i in groups]

def never_down(pw):
    return all([ord(pw[i]) <= ord(pw[i+1]) for i in range(5)])

def is_valid_password(pw):
    return never_down(pw) and duplicated(pw)

def ex1(start, end):
    pw_range = range(start, end + 1)
    valid_pws = [pw for pw in pw_range if is_valid_password(str(pw))]
    return len(valid_pws)

print(ex1(382345, 843167))

