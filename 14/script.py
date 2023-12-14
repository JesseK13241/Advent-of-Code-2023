# Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?

from enum import Enum
class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    WEST = "west"
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
    
    print(f"\nBefore (tilt={direction}):")
    print("\n".join(lines))
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
    
    print(f"\nAfter:")
    print("\n".join(new_lines))
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

    print(f"\nTotal load is {total_load} (direction={direction})\n")
    return total_load

'''
load_example = ["O#OO", "O.##", "O.#."]
for direction in Direction:
    total_load = calculate_load(load_example, direction)
exit()

for direction in Direction:
    tilt_platform(lines, direction)
'''

direction = Direction.NORTH
tilted_north = tilt_platform(lines, direction)
calculate_load(tilted_north, direction)
