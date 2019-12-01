def fuel_for_mass(m):
    return int(m / 3) - 2

def adjust(fuel):
    fuel_for_fuel = fuel_for_mass(fuel)
    if fuel_for_fuel <= 0:
        return fuel
    else:
        return fuel + adjust(fuel_for_fuel)

masses = [int(x) for x in open("input.txt").readlines()]

fuels = [adjust(fuel_for_mass(m)) for m in masses]
totalFuel = sum(fuels)
print(totalFuel)
