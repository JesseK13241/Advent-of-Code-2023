# Starting from the garden plot marked S on your map, how many garden plots could the Elf reach in exactly 64 steps?

import sys
from copy import deepcopy

data_file = sys.argv[1]

step_count = 64

"""
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

with open(data_file) as f:
    lines = f.read().splitlines()

lines = [list(line) for line in lines]

grid = list[list[str]]
loc = tuple[int, int]

start_location = (0, 0)

width, height = len(lines[0]), len(lines)
for y in range(height):
    for x in range(width):
        if lines[y][x] == "S":
            start_location = (x, y)
            print(f"Start location found at {start_location}")
            break
    else:
        continue
    break


def get_nearby_cells(grid: grid, loc: loc) -> list[tuple[loc, str]]:
    x, y = loc
    width, height = len(grid[0]), len(grid)
    nearby_tiles = []
    if y > 0:
        above = grid[y - 1][x]
        nearby_tiles.append(((x, y - 1), above))
    if y + 1 < height:
        below = grid[y + 1][x]
        nearby_tiles.append(((x, y + 1), below))
    if x + 1 < width:
        right = grid[y][x + 1]
        nearby_tiles.append(((x + 1, y), right))
    if x > 0:
        left = grid[y][x - 1]
        nearby_tiles.append(((x - 1, y), left))

    # print(f"nearby cells of {loc} are {nearby_tiles}")
    return nearby_tiles


def advance(grid: grid) -> grid:
    # replace nearby plots (. or S) with O for every O or S
    # replace current tile with .
    copy = deepcopy(grid)
    width, height = len(grid[0]), len(grid)
    for y in range(height):
        for x in range(width):
            all_nearby_plots = []
            if grid[y][x] in ["O", "S"]:
                # print(f"Cell at {(x,y)} is {grid[y][x]}")
                nearby_plots = get_nearby_cells(grid, (x, y))
                all_nearby_plots.extend(nearby_plots)
            for nearby_plot in all_nearby_plots:
                loc, tile_type = nearby_plot
                nearby_x, nearby_y = loc
                if tile_type in ["S", "."]:
                    # print(f"Placing O to {(nearby_x, nearby_y)}")
                    copy[nearby_y][nearby_x] = "O"
                copy[y][x] = "."

    start_x, start_y = start_location
    above = copy[start_y - 1][start_x]
    if above == "O":
        copy[start_y][start_x] = "S"
    else:
        copy[start_y][start_x] = "O"
    print(f"Mid = {copy[start_y][start_x]}")
    return copy


def calculate_gardens(grid: grid) -> int:
    total = 0
    for line in grid:
        total += line.count("O")
    return total


def print_grid(grid: grid) -> None:
    lines = ["".join(line) for line in grid]
    print("\n".join(lines))
    print()


print_grid(lines)
for step in range(step_count):
    lines = advance(lines)
    print(f"\nAfter step {step+1}")
    print_grid(lines)
    result = calculate_gardens(lines)
    print(f"Total of {result} garden plots could be reached in exactly {step+1} steps.")
