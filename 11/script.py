# Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

import itertools

with open("input") as f:
    lines = f.read().splitlines()

empty_space = "."
galaxy = "#"

print("\nImage:")
print("\n".join(lines))

def transpose(lines: list[str]) -> list[str]:
    return ["".join(line) for line in zip(*lines)]

def get_vertical_expansion_indices(lines: list[str]) -> list[int]:
    height, width = len(lines), len(lines[0])
    empty_row_indices = list(range(height))
    for y in range(height):
        for x in range(width):
            if lines[y][x] == galaxy:
                empty_row_indices.remove(y)
                break # Skip galaxies on the same row
    return empty_row_indices

def expand_vertically(lines: list[str]) -> list[str]:
    height, width = len(lines), len(lines[0])
    print(get_vertical_expansion_indices(lines))
    empty_rows = get_vertical_expansion_indices(lines)
    vertical_expansion = []
    for row in range(height):
        if row in empty_rows:
            vertical_expansion.append(empty_space * width)
            vertical_expansion.append(empty_space * width)
        else:
            vertical_expansion.append(lines[row])

    return vertical_expansion

def expand_empty_lines(lines: list[str]) -> list[str]:
    vertical_expansion = expand_vertically(lines)
    print("\nVertical expansion:")
    print("\n".join(vertical_expansion))

    total_expansion = expand_vertically(transpose(vertical_expansion))
    total_expansion = transpose(total_expansion)
    
    print("\nTotal expansion:")
    print("\n".join(total_expansion))
    return total_expansion

def get_galaxies(lines: list[str]) -> list[tuple[int, int]]:
    height, width = len(lines), len(lines[0])
    new_lines = []
    galaxies = []
    counter = 1
    for y in range(height):
        new_line = []
        for x in range(width):
            if lines[y][x] == galaxy:
                new_line.append(str(counter))
                galaxies.append((x, y))
                counter += 1
            else:
                new_line.append(empty_space)
        new_lines.append("".join(new_line))
    
    print("\nNumbered:")
    print("\n".join(new_lines))
    return galaxies
'''
galaxies = get_galaxies(expand_empty_lines(lines))

print("\nGalaxies:")
print(galaxies)
# [(4, 0), (9, 1), (0, 2), (8, 5), (1, 6), (12, 7), (9, 10), (0, 11), (5, 11)]

pairs_of_galaxies = list(itertools.combinations(galaxies, 2))
print(f"\n{len(pairs_of_galaxies)} pairs of galaxies")

total_distance = 0
for pair in pairs_of_galaxies:
    galaxy_a, galaxy_b = pair
    x_diff = abs(galaxy_a[0] - galaxy_b[0])
    y_diff = abs(galaxy_a[1] - galaxy_b[1])
    distance = x_diff + y_diff
    #print(f"Distance of {galaxy_a} and {galaxy_b} is {distance}")
    total_distance += distance

print(f"\nTotal distance sum is {total_distance}")

# Part 2: Starting with the same initial image, expand the universe one million times, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
'''

galaxies = get_galaxies(lines)

vertical_expansion_indices = get_vertical_expansion_indices(lines)
horizontal_expansion_indices = get_vertical_expansion_indices(transpose(lines))
print(f"\nEmpty space (vertical): {vertical_expansion_indices}")
print(f"Empty space (horizontal): {horizontal_expansion_indices}")

print("\nGalaxies:")
print(galaxies)
# [(4, 0), (9, 1), (0, 2), (8, 5), (1, 6), (12, 7), (9, 10), (0, 11), (5, 11)]

pairs_of_galaxies = list(itertools.combinations(galaxies, 2))
print(f"\n{len(pairs_of_galaxies)} pairs of galaxies")

expansion = 1000000
total_distance = 0
for pair in pairs_of_galaxies:
    galaxy_a, galaxy_b = pair
    x_diff = abs(galaxy_a[0] - galaxy_b[0])
    y_diff = abs(galaxy_a[1] - galaxy_b[1])
    distance = x_diff + y_diff

    for index in horizontal_expansion_indices:
        if (galaxy_a[0] < index < galaxy_b[0]) or (galaxy_a[0] > index > galaxy_b[0]):
            # print(f"Empty horizontal space (at {index}) between {galaxy_a} and {galaxy_b}")
            distance += (expansion-1)

    for index in vertical_expansion_indices:
        if (galaxy_a[1] < index < galaxy_b[1]) or (galaxy_a[1] > index > galaxy_b[1]):
            # print(f"Empty vertical space (at {index}) between {galaxy_a} and {galaxy_b}")
            distance += (expansion-1)

    # print(f"Distance of {galaxy_a} and {galaxy_b} is {distance}\n")
    total_distance += distance

print(f"\nTotal distance sum is {total_distance} (expansion={expansion}x)")