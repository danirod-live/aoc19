from collections import defaultdict

def read_recipe():
    def read_recipe_line(line):
        in_chem, out_chem = line.strip().split(" => ")
        in_chems = in_chem.split(", ")
        return (
            tuple([c.split(" ") for c in in_chems]),
            tuple(out_chem.split(" ")),
        )
    recipes = [
        read_recipe_line(l)
        for l in open("input.txt").readlines()
    ]
    return {
        r[1][1]: (int(r[1][0]), list((int(c), m) for c, m in r[0]))
        for r in recipes
    }

recipes = read_recipe()

def make(count, material, stash, ores):
    # Primitive material has to be bought
    if material == 'ORE':
        return ores + count

    # We have enough of this to not require to make some
    if material in stash and stash[material] >= count:
        stash[material] -= count
        return ores

    # Otherwise we have to build it
    units_to_gain, recipe_for_material = recipes[material]
    for sub_count, sub_material in recipe_for_material:
        ores = make(sub_count, sub_material, stash, ores)
    stash[material] += units_to_gain
    return make(count, material, stash, ores)

ores = make(1, "FUEL", defaultdict(int), 0)
print(ores)


def consume(count, material, stash, ores):
    # Primitive material has to be bought
    if material == 'ORE':
        if ores < count:
            raise AttributeError("Not enough money")
        return ores - count

    # We have enough of this to not require to make some
    if material in stash and stash[material] >= count:
        stash[material] -= count
        return ores

    # Otherwise we have to build it
    units_to_gain, recipe_for_material = recipes[material]
    for sub_count, sub_material in recipe_for_material:
        ores = consume(sub_count, sub_material, stash, ores)
    stash[material] += units_to_gain
    return consume(count, material, stash, ores)

ores = 1000000000000
inventory = defaultdict(int)
fuel = 0
try:
    while True:
        ores = consume(1, "FUEL", inventory, ores)
        fuel += 1
except AttributeError:
    pass
print(fuel)
