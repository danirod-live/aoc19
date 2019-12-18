def position(map2d, key):
    charmap = map2d.split("\n")
    row = [i for i in range(len(charmap)) if key in charmap[i]][0]
    return (charmap[row].index(key), row)

def compute_map(map2d):
    DELTA = [(1, 0), (-1, 0), (0, 1), (0, -1)]
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
    keys = [k for k in map2d if 'a' <= k <= 'z' or k == '@']
    return {key: keys_i_can_visit(map2d, key) for key in keys}

def available_keys(graph, key, keychain, visited=None):
    if not visited:
        visited = set(key)

    # Get keys visible from my current spot.
    key_queue = list(graph[key])
    candidates = {}
    while key_queue:
        target_key, distance, keys_required = key_queue.pop()

        # Don't revisit a key twice.
        if target_key in visited:
            continue

        # I cannot pick keys that are behind doors I cannot open.
        if len(set(keys_required).difference(keychain)) > 0:
            continue

        # If the key is in my keychain, they doesn't really exist.
        if target_key in keychain:
            visited.add(target_key)
            key_queue += [
                (key, distance + sub_d, keys_required)
                for key, sub_d
                in available_keys(graph, target_key, keychain, visited)
            ]
            visited.remove(target_key)
            continue

        if target_key not in candidates:
            candidates[target_key] = distance
        else:
            candidates[target_key] = min(candidates[target_key], distance)
    return candidates.items()

def best_decision(map2d):
    graph = compute_map(map2d)

    def memokey(keychain):
        lst = list(keychain)
        lst.sort()
        return "".join(lst)

    def step(leaves):
        memo = {}
        out = {}
        for keychain, dist, last in leaves:
            memo_key = memokey(keychain)
            if (last + memo_key) in memo:
                next_leaves = memo[(last + memo_key)]
            else:
                next_leaves = available_keys(graph, last, keychain)
                memo[last + memo_key] = next_leaves
            for key, distance in next_leaves:
                out_key = key + memokey(keychain.union(key))
                if out_key not in out:
                    out[out_key] = dist + distance
                else:
                    out[out_key] = min(out[out_key], dist + distance)
        return [(set(k[1:]), v, k[0]) for k,v in out.items()]

    leaves = available_keys(graph, "@", set())
    leaves = [(set(key), dist, key) for key, dist in leaves]
    i = 0
    while leaves:
        print(i)
        i += 1
        next_leaves = step(leaves)
        if not next_leaves:
            return min(leaves, key=lambda d: d[1])
        else:
            leaves = next_leaves

CASE = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

case = open("input.txt").read().strip()

graph = compute_map(CASE)
print(best_decision(case))
