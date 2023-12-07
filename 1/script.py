'''
On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

'''

def get_indices(line: str, search_term: str) -> list[int]:
    indices = [i for i in range(len(line)) if line.startswith(search_term, i)]
    return indices

def get_first_and_last_digits(line: str) -> tuple[str, str] | None:
    
    print()
    print(f"line {line}")
    indices = {}
    
    digits = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
    for digit in digits.keys():
        try: 
            digit_indices = get_indices(line, digit)
            for digit_index in digit_indices:
                indices[digit_index] = digit
        except ValueError:
            continue
    
    # 2three5three --> indices = {1: three, 7: 'three}
    # eightwothree --> indices = {4: 'two', 7: 'three', 0: 'eight'}
    # eighthree --> indices = {4: 'three', 0: 'eight'}
    
    print(f"indices {indices}")

    first_digit = None
    last_digit = None

    first_spelled_digit = None
    last_spelled_digit = None
    
    try:
        first_spelled_digit = min(indices)
    except ValueError:
        pass
        
    if first_spelled_digit == None:
        for symbol in line:
            if symbol.isdigit():
                first_digit = symbol
                break
    else:
        for symbol in line[:first_spelled_digit]:
            if symbol.isdigit():
                first_digit = symbol
                break
            
        if first_digit == None:
            first_digit = str(digits[indices[first_spelled_digit]])
        
    try:
        last_spelled_digit = max(indices)
    except ValueError:
        pass

    if last_spelled_digit == None:
        for symbol in line[::-1]:
            if symbol.isdigit():
                last_digit = symbol
                break
    else:
        for symbol in line[:last_spelled_digit:-1]:
            if symbol.isdigit():
                last_digit = symbol
                break

        if last_digit == None:
            last_digit = str(digits[indices[last_spelled_digit]])
    
    if first_digit and last_digit:
        return (first_digit, last_digit)
    else:
        return None

with open("input") as f:
    lines = f.read().splitlines()
    
total = 0

for line in lines:

    line_digits = get_first_and_last_digits(line)
    if line_digits:
        first_digit, last_digit = line_digits
        value = int(first_digit + last_digit)
        print(f"Digits {first_digit} & {last_digit}")
        total += value
    else:
        print(f"Digits not found on line: {line}")
        break
    
print(f"Total = {total}")