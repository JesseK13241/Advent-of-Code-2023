'''Any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

What is the sum of all of the part numbers in the engine schematic?
'''

with open("input") as f:
    lines = f.read().splitlines()

# for every number (1 or more digits)
# get location (x=first number line index,y=row)

numbers = {}
# {(0, 0): '4', ... , (7, 9): '8'}

symbols = {}
# {(3, 1): '*', ... , (5, 8): '*'}

max_x = len(lines[0])
max_y = len(lines)

for y in range(max_y):
    for x in range(max_x):
        char = lines[y][x]
        if char == ".":
            continue
        elif char.isdigit():
            numbers[(x,y)] = char
        else: # symbol
            symbols[(x,y)] = char

loc = tuple[int, int]
def get_start_locations(numbers: dict[loc, str]) -> dict[loc, tuple[str, loc]]:
    # {(0, 0): '4', ... , (7, 9): '8'}
    # --> {(0, 0): ('4', (0, 0)), (1, 0): ('6', (0, 0)), ... , }
    numbers_with_start_loc = {}
    for number_loc, number in numbers.items():
        x, y = number_loc
        leftseek = 1
        print(f"loc of {number} is {number_loc}")
        while (x-leftseek,y) in numbers:
            print(f"digit on the left found: {numbers[x-leftseek,y]}")
            leftseek += 1
        start_loc = (x-leftseek+1, y)
        print(f"start loc is {start_loc}\n")
        numbers_with_start_loc[number_loc] = (number, start_loc)

    return numbers_with_start_loc

numbers_with_start_loc = get_start_locations(numbers)
start_locs_of_numbers_near_symbols = []
number_start_locs_by_symbol_loc = {symbol:[] for symbol in symbols} # part 2
# # {(3, 1): [], ... , (5, 8): []}

for symbol_loc, symbol in symbols.items():
    x, y = symbol_loc
    for xd in (-1, 0, 1):
        for yd in (-1, 0, 1):
            if (x+xd, y+yd) in numbers_with_start_loc:
                digit, start_loc = numbers_with_start_loc[(x+xd, y+yd)]
                print(f"Digit {digit} (start loc = {start_loc}) near {symbol} ({symbol_loc})")
                start_locs_of_numbers_near_symbols.append(start_loc)
                number_start_locs_by_symbol_loc[symbol_loc].append(start_loc)

def get_number_from_start_loc(start_loc: loc) -> int:
    x, y = start_loc
    number_as_string = numbers[start_loc]
    rightseek = 1
    while (x+rightseek, y) in numbers:
        number_as_string += numbers[x+rightseek, y]
        rightseek += 1
    
    return int(number_as_string)

total1 = 0
for number_start_log in set(start_locs_of_numbers_near_symbols):
    number = get_number_from_start_loc(number_start_log)
    total1 += number

print(f"\nTotal1 = {total1}")

''' Part 2
A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

What is the sum of all of the gear ratios in your engine schematic? '''

total2 = 0
for symbol_loc, start_locs in number_start_locs_by_symbol_loc.items():
    unique_start_locs = set(start_locs)
    if len(unique_start_locs) == 2:
        first_loc, second_loc = unique_start_locs
        first_num, second_num = map(get_number_from_start_loc, (first_loc, second_loc))
        total2 += (first_num * second_num)

print(f"\nTotal2 = {total2}")