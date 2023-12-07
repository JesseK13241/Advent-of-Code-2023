'''
Cach card has two lists of numbers separated by a vertical bar (|): a list of winning numbers and then a list of numbers you have. 

You have to figure out which of the numbers you have appear in the list of winning numbers. The first match makes the card worth one point and each match after the first doubles the point value of that card.
'''

def calculate_point(line: str) -> int:
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    # --> 8 points
    card_id, numbers = line.split(":")
    card_id = card_id.split()[-1]
    winning_numbers, found_numbers = numbers.split("|")
    winning_numbers = winning_numbers.split()
    found_numbers = found_numbers.split()
    matches = 0
    for number in found_numbers:
        if number in winning_numbers:
            matches += 1 

    if matches:
        points = 2 ** (matches-1)
        print(f"Card {card_id} is worth {points} points")
        return points
    else:
        return 0

with open("input") as f:
    lines = f.read().splitlines()

total_points = 0
for line in lines:
    points = calculate_point(line)
    total_points += points

print(f"Total points: {total_points}")

''' # Part 2
There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have.

Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.'''

cards = lines.copy()

def calculate_bonus_cards(line: str) -> int: # part 2
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    # --> 
    card_id, numbers = line.split(":")
    card_id = int(card_id.split()[-1])
    winning_numbers, found_numbers = numbers.split("|")
    winning_numbers = winning_numbers.split()
    found_numbers = found_numbers.split()
    matches = 0
    for number in found_numbers:
        if number in winning_numbers:
            matches += 1 

    bonus_cards = 1
    if matches:
        for i in range(matches):
            if card_id + i < len(cards):
                bonus_cards += calculate_bonus_cards(cards[card_id + i])
    
    return bonus_cards

total_cards = 0
for line in lines:
    bonus_cards = calculate_bonus_cards(line)
    total_cards += bonus_cards

print(f"Total cards: {total_cards}")
