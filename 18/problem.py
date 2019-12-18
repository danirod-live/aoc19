def position(map2d, key):
    charmap = map2d.split("\n")
    row = [i for i in range(len(charmap)) if key in charmap[i]][0]
    return (charmap[row].index(key), row)

def available_keys(map2d, position, keychain):
    charmap = map2d.split("\n")

    def neirghbours(x, y):
        return [(x+dx, y+dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

    def find_keys(x, y, visited=None):
        # Keep a list of visited nodes to avoid infinite loops.
        if not visited:
            visited = set()
            visited.add((x, y))

        keys = []
        for cx, cy in neirghbours(x, y):
            # Don't look twice for the same spot.
            if (cx, cy) in visited:
                continue

            cell = charmap[cy][cx]
            is_key = 'a' <= cell <= 'z'
            is_door = 'A' <= cell <= 'Z'
            is_gap = cell in ('.', '@')

            can_walk_over = any([
                is_gap,
                is_key and cell in keychain,
                is_door and cell.lower() in keychain,
            ])
            if is_key and cell not in keychain:
                # This is a key we haven't picked yet.
                keys.append((cell, 1))
            if can_walk_over:
                # This is a position I can walk to.
                visited.add((cx, cy))
                keys += [(k, d + 1) for k, d in find_keys(cx, cy, visited)]
                visited.remove((cx, cy))
        return keys

    px, py = position
    return find_keys(px, py)

def best_decision(map2d):
    def step(leaves):
        memo = {}
        out = {}
        for keychain, dist, last in leaves:
            pos = position(map2d, last)
            memo_key = "".join(keychain)
            if (last + memo_key) in memo:
                next_leaves = memo[(last + memo_key)]
            else:
                next_leaves = available_keys(map2d, pos, keychain)
                memo[last + memo_key] = next_leaves
            for key, distance in next_leaves:
                out_key = key + "".join(keychain.union(key))
                if out_key not in out:
                    out[out_key] = dist + distance
                else:
                    out[out_key] = min(out[out_key], dist + distance)
        return [(set(k[1:]), v, k[0]) for k,v in out.items()]

    at = position(map2d, "@")
    leaves = available_keys(map2d, at, set())
    leaves = [(set(key), dist, key) for key, dist in leaves]
    while True:
        print(len(leaves), leaves[0])
        next_leaves = step(leaves)
        if not next_leaves:
            return min(leaves, key=lambda d: d[1])
        leaves = next_leaves

CASE = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

case = open("input.txt").read().strip()
print(best_decision(case))
