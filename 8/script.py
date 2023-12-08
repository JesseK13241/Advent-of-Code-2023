# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

with open("input") as f:
    lines = f.read().splitlines()

instructions = lines[0]

elements : dict[str, tuple[str, str]] = {} 
# {'AAA': ('BBB', 'CCC'), 'BBB': ('DDD', 'EEE'), 'CCC': ('ZZZ', 'GGG'), 'DDD': ('DDD', 'DDD'), 'EEE': ('EEE', 'EEE'), 'GGG': ('GGG', 'GGG'), 'ZZZ': ('ZZZ', 'ZZZ')}

for line in lines[2:]:
    element, left_and_right = line.split(" = ")
    left, right = left_and_right[1:-1].split(", ")
    elements[element] = (left, right)

'''
start = "AAA"
end = "ZZZ"

location = start
steps = 1

while True:
    if location == end:
        print(f"End reached after {steps} steps")
        break
    for direction in instructions:
        if location == end:
            print(f"End reached after {steps} steps")
            break
        print(f"Currently at {location}")
        next_location = ""
        if direction == "L":
            next_location = elements[location][0]
            print(f"Going left to {next_location}")
        elif direction == "R":
            next_location = elements[location][1]
            print(f"Going right to {next_location}")
        location = next_location
        print(f"Step {steps} done")
        print("")
        steps += 1
'''

# Part 2: Start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

paths = {}
for element, directions in elements.items():
    if element.endswith("A"):
        paths[element] = directions

print(f"instructions: {instructions}\n")

def progress_path(element: str, instruction: str) -> None:
    print(f"Progressing path {element} to the {instruction}")
    if instruction == "L":
        next_element = paths[element][0]
    else:
        next_element = paths[element][1]

    del paths[element]
    paths[next_element] = elements[next_element]

def all_finished() -> bool:
    return all([path.endswith("Z") for path in paths])

'''
cache = {} # for infinite loop detection

while True:
    index = 0
    if all_finished():
        print(f"End reached after {steps} steps")
        break
    for direction in instructions:
        temp_paths = dict(paths)
        for path in temp_paths:
            progress_path(path, direction)
        print(f"After step {steps}: {paths}\n")
        if all_finished():
            break
        steps += 1

        cache_key = tuple(paths.keys())
        print(cache_key)
        if cache_key in cache:
            if cache[cache_key] == index:
                print("Infinite loop detected!")
                print(cache)                
        else:
            cache[cache_key] = index
        index += 1

'''

# Takes too long --> Check each path separately and analyze

print(f"elements: {elements}\n")

path_lengths = []
remaining_paths = list(paths.keys())

def get_next_direction(steps: int) -> int:
    if steps:
        steps = steps % len(instructions)
    next_direction = instructions[steps]
    if next_direction == "L":
        return 0
    else:
        return 1

steps = 0
while remaining_paths:
    print(f"\nStep {steps}: Remaining paths: {remaining_paths}")
    next_direction = get_next_direction(steps)
    print(f"direction = {next_direction}\n")
    new_paths = []
    for path in remaining_paths:
        if path.endswith("Z"):
            print(f"Path {path} finished after {steps} steps")
            path_lengths.append(steps)
        else:
            next_location = elements[path][next_direction]
            print(f"{path} becomes {next_location}")
            new_paths.append(next_location)
    
    print(f"={new_paths}")
    remaining_paths = new_paths.copy()
    steps += 1

import numpy as np
print(f"\nPath lengths: {path_lengths}")
print(f"LCM (numpy) = {np.lcm.reduce(path_lengths)}")
# overflows to negative

from math import lcm
print(f"LCM (python)= {lcm(*path_lengths)}")