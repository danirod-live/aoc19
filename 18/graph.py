DELTA = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def position(map2d, key):
    charmap = map2d.split("\n")
    row = [i for i in range(len(charmap)) if key in charmap[i]][0]
    return (charmap[row].index(key), row)

def keys_i_can_visit(map2d, key):
    charmap = map2d.split("\n")

    def find_keys(x, y, visited=None):
        # Keep a list of visited nodes to avoid infinite loops.
        if not visited:
            visited = {(x, y)}

        keys = []
        for dx, dy in DELTA:
            cx, cy = x + dx, y + dy

            # Don't look twice
            if (cx, cy) in visited:
                continue

            cell = charmap[cy][cx]

            if 'a' <= cell <= 'z':
                keys.append((cell, 1, []))
            if 'A' <= cell <= 'Z':
                # Assume you can get in as long as you have the key
                visited.add((cx, cy))
                keys += [
                    (key, dist + 1, doors + [cell.lower()])
                    for key, dist, doors in find_keys(cx, cy, visited)
                ]
                visited.remove((cx, cy))
            if cell == '.' or cell == '@':
                # It's air.
                visited.add((cx, cy))
                keys += [
                    (key, dist + 1, doors)
                    for key, dist, doors in find_keys(cx, cy, visited)
                ]
                visited.remove((cx, cy))
        return keys
    ox, oy = position(map2d, key)
    return find_keys(ox, oy)

def compute_map(map2d):
    keys = [k for k in map2d if 'a' <= k <= 'z' or k == '@']
    return {key: keys_i_can_visit(map2d, key) for key in keys}


data = open("input.txt").read().strip()

MAP = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

print(compute_map(MAP))
