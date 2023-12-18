# The Elves are concerned the lagoon won't be large enough;
# if they follow their dig plan, how many cubic meters of lava could it hold?

import os
import sys
from enum import Enum
from PIL import Image, ImageDraw, ImageFont

data = sys.argv[1]


class Direction(Enum):
    UP = "U"
    RIGHT = "R"
    DOWN = "D"
    LEFT = "L"


direction_mapping = {
    "U": Direction.UP,
    "R": Direction.RIGHT,
    "D": Direction.DOWN,
    "L": Direction.LEFT,
}

with open(data) as f:
    lines = f.read().splitlines()
    # R 6 (#70c710)

Grid = list[list[str]]
dig: Grid = [["#"]]
loc = tuple[int, int]
position: loc = (0, 0)


def create_image_from_2d_list(data, output_file, cell_size=20, font_size=12) -> None:
    # by Chat-GPT

    # Calculate the dimensions of the image based on the 2D list
    width = len(data[0]) * cell_size
    height = len(data) * cell_size

    # Create a new image with a white background
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Load a font for text rendering
    font = ImageFont.truetype("arial.ttf", font_size)

    # Iterate through the 2D list and draw the text on the image
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            x = j * cell_size
            y = i * cell_size
            draw.text((x, y), cell, font=font, fill="black")

    # Save the image to a file
    image.save(output_file)
    print(f"Image saved to '{output_file}'")


def clear_console() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_grid(grid: Grid) -> None:
    grid_as_text = []
    for line in grid:
        grid_as_text.append("".join(line))
    print("\n".join(grid_as_text))


def get_next_dig(dig: Grid, position: loc, direction: Direction) -> tuple[Grid, loc]:
    x, y = position
    next_position = position
    width, height = len(dig[0]), len(dig)

    if direction == Direction.RIGHT:
        if width == x + 1:
            # Add line to the right
            for line in dig:
                line.append(".")
        dig[y][x + 1] = "#"
        next_position = (x + 1, y)

    elif direction == Direction.DOWN:
        if height == y + 1:
            # Add line to the bottom
            dig.append(list("." * width))
        dig[y + 1][x] = "#"
        next_position = (x, y + 1)

    elif direction == Direction.LEFT:
        if x == 0:
            # Add line to the left
            for line in dig:
                line.insert(0, ".")
            dig[y][x] = "#"
        else:
            dig[y][x - 1] = "#"
            next_position = (x - 1, y)

    elif direction == Direction.UP:
        if y == 0:
            # Add line to the top
            dig.insert(0, list("." * width))
            dig[y][x] = "#"
        else:
            dig[y - 1][x] = "#"
            next_position = (x, y - 1)

    return dig, next_position


for line in lines:
    direction_char, distance, color = line.split()
    direction = direction_mapping[direction_char]
    for i in range(int(distance)):
        next_dig, next_position = get_next_dig(dig, position, direction)
        # clear_console()
        dig = next_dig
        position = next_position

# create_image_from_2d_list(dig, output_file=f"{data} visualization.png")


def flood_fill(grid: Grid, location: loc) -> None:
    x, y = location
    if grid[y][x] == ".":
        grid[y][x] = "#"

    try:
        up = grid[y - 1][x]
        if up == ".":
            flood_fill(grid, (x, y - 1))
    except IndexError:
        pass

    try:
        right = grid[y][x + 1]
        if right == ".":
            flood_fill(grid, (x + 1, y))
    except IndexError:
        pass

    try:
        down = grid[y + 1][x]
        if down == ".":
            flood_fill(grid, (x, y + 1))
    except IndexError:
        pass

    try:
        left = grid[y][x - 1]
        if left == ".":
            flood_fill(grid, (x - 1, y))
    except IndexError:
        pass


def fill_grid(grid: Grid) -> None:
    # Scan the grid starting from the top+1:
    # If pattern #. is found, flood fill start is at .
    width, height = len(grid[0]), len(grid)
    print(f"Grid is {width}x{height}")
    sys.setrecursionlimit(width * height)  # default = 1000
    prev_char = ""

    for y in range(1, height):
        for x in range(width):
            this_char = grid[y][x]
            if this_char == "." and prev_char == "#":
                print(f"Fill starting at {(x, y)}")
                flood_fill(grid, (x, y))
                return None
            prev_char = this_char


dig_path_length = 0
for line in dig:
    dig_path_length += line.count("#")
print(f"dig path length = {dig_path_length}")

dig_volume = 0
fill_grid(dig)
for line in dig:
    dig_volume += line.count("#")
print(f"dig volume = {dig_volume}")

create_image_from_2d_list(dig, output_file=f"{data} filled.png")
