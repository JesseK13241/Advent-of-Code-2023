# Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?

from enum import Enum
class Direction(Enum):
    NORTH = "north"
    WEST = "west"
    SOUTH = "south"
    EAST = "east"

with open("input") as f:
    lines = f.read().splitlines()

def transpose(lines: list[str]) -> list[str]:
    return ["".join(line) for line in zip(*lines)]

def tilt_line(line: str, direction: Direction = Direction.WEST) -> str:
    # Moves the movable characters to the left or the right of the string
    # ..O..#O..O --> O....#OO..
    new_line_parts = []
    for line_part in line.split("#"):
        movable_characters: str = line_part.count("O") * "O"
        if direction == Direction.WEST:
            new_line_part = movable_characters.ljust(len(line_part), ".")
        elif direction == Direction.EAST:
            new_line_part = movable_characters.rjust(len(line_part), ".")
        else:
            print(f"Direction {direction} not supported for a line.")
            return ""
        new_line_parts.append(new_line_part)
    return "#".join(new_line_parts)

def tilt_platform(lines: list[str], direction: Direction) -> list[str]:
    # Moves the movable characters in a string matrix to any direction
    
    #print(f"\nBefore (tilt={direction}):")
    #print("\n".join(lines))
    new_lines = []

    transpose_needed = False
    if direction in [Direction.NORTH, Direction.SOUTH]:
        transpose_needed = True

    match direction:
        case Direction.SOUTH:
            direction = Direction.EAST
        case Direction.EAST:
            direction = Direction.EAST
        case Direction.NORTH:
            direction = Direction.WEST
    
    if transpose_needed:
        lines = transpose(lines)
    for line in lines:
        new_lines.append(tilt_line(line, direction))
    if transpose_needed:
        new_lines = transpose(new_lines)
    
    #print(f"\nAfter:")
    #print("\n".join(new_lines))
    return new_lines

def calculate_load(lines: list[str], direction: Direction) -> int:
    # Calculates the load of movable characters ("O")
    # O#OO 3
    # O.## 2
    # O.#. 1
    # North load = 12
    # South load = 8
    # West load = 15
    # East load = 10
    
    total_load = 0

    if direction in [Direction.WEST, Direction.EAST]:
        lines = transpose(lines)

    if direction in [Direction.SOUTH, Direction.EAST]:
        lines = lines[::-1]

    maximum_load = len(lines)
    for line in lines:
        total_load += line.count("O") * maximum_load
        maximum_load -= 1

    print(f"Total load is {total_load} (direction={direction})")
    return total_load

''' testing code
load_example = ["O#OO", "O.##", "O.#."]
for direction in Direction:
    total_load = calculate_load(load_example, direction)
exit()
'''

''' Part 1
direction = Direction.NORTH
tilted_north = tilt_platform(lines, direction)
calculate_load(tilted_north, direction)
'''

# Part 2
# Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. 
# Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?

tilted = lines
cycle = 0
max_cycles = 1000000000
configurations = [tilted]
loads = [calculate_load(tilted, Direction.NORTH)]
cycle_start = 0
cycle_end = 0

while cycle < max_cycles:
    for direction in Direction:
        tilted = tilt_platform(tilted, direction)

    cycle += 1    
    #print(f"\nAfter {cycle} cycles:")
    #print("\n".join(tilted))

    load = calculate_load(tilted, Direction.NORTH)
    if tilted in configurations:
        duplicate_cycle = configurations.index(tilted)
        print(f"Cycle {cycle} is identical to cycle {duplicate_cycle}")
        cycle_start = duplicate_cycle
        cycle_end = cycle-1
        break

    configurations.append(tilted)
    loads.append(load)
    print(f"{len(configurations)} configurations")

print(f"\nLoads: {loads} (len={len(loads)})")
print(f"Cycle start at {cycle_start}: {loads[cycle_start]}")
print(f"Cycle end at {cycle_end}: {loads[cycle_end]}")

pre_cycle_length = cycle_start
cycle_length = cycle_end - cycle_start + 1
offset = (max_cycles - pre_cycle_length) % cycle_length
load_at_max_cycle = loads[cycle_start+offset]
print(f"Load at max cycle ({max_cycles}) = {load_at_max_cycle}")
