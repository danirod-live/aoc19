def read(file):
    orbits = [l.strip() for l in open(file).readlines()]
    parents = {orbit.split(')')[1]: orbit.split(')')[0] for orbit in orbits}
    return parents

file = "input2.txt"
parents = read(file)

def orbits(x):
    if x not in parents.keys():
        return 0
    else:
        return 1 + orbits(parents[x])

checksum = sum([orbits(x) for x in parents.keys()])


def chain(x):
    if x not in parents.keys():
        return [x]
    else:
        return [x] + chain(parents[x])

def nearest_common_ancestor(node1, node2):
    chain1 = chain(node1)
    chain2 = chain(node2)
    for item in chain1:
        if item in chain2:
            return item
    return None

node1 = parents["YOU"]
node2 = parents["SAN"]
chain1 = chain(node1)
chain2 = chain(node2)
common = nearest_common_ancestor(node1, node2)
print(chain1.index(common) + chain2.index(common))
