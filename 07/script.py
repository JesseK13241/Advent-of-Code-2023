# Find the rank of every hand in your set. What are the total winnings?

import functools, random
from collections import Counter

with open("input") as f:
    lines = f.read().splitlines()

hands_and_bids = {line.split()[0]: int(line.split()[1]) for line in lines}
# {'32T3K': 765, 'T55J5': 684, 'KK677': 28, 'KTJJT': 220, 'QQQJA': 483}

print("Hands and bids:")
print(hands_and_bids)

def card_value(card: str) -> int:
    possible_cards = "AKQT98765432J"[::-1]
    assert len(card) == 1
    return possible_cards.index(card)

def hand_type_value(hand: str, show=False) -> float:
        
    assert len(hand) == 5
    jokers = hand.count("J")
    cards = Counter(hand)
    count = cards.most_common()[0][1]

    if count == 5:
        return 5 # five of a kind
    if count == 4:
        if jokers:
            return 5
        return 4 # four of a kind
    if len(cards) == 2 and count == 3: #AAABB
        if jokers:
            return 5
        return 3.5 # full house
    if len(cards) == 3:
        if count == 3: # AAABC
            if jokers:
                return 4
            else:
                return 3
        if count == 2: # AABBC
            if jokers == 2:
                return 4
            if jokers == 1:
                return 3.5
            return 2
    if len(cards) == 4: #AABCD
        if jokers:
            return 3 
        return 1
    if len(cards) == 5: #ABCDE
        if jokers:
            return 1
        return 0
    return -1

def compare_hands(hand1: str, hand2: str) -> int:
    # sort by type, then by the card value
    if hand_type_value(hand1) > hand_type_value(hand2):
        # print(f"Hand value for {hand1} > {hand2}: {hand_type_value(hand1)} > {hand_type_value(hand2)}")
        return 1
    elif hand_type_value(hand1) < hand_type_value(hand2):
        # print(f"Hand value for {hand2} > {hand1}: {hand_type_value(hand2)} > {hand_type_value(hand1)}")
        return -1
    else:
        print(f"Hand value for {hand1} = {hand2}: {hand_type_value(hand1)}")
        for i in range(len(hand1)):
            if card_value(hand1[i]) > card_value(hand2[i]):
                # print(f"Card value for {hand1} > {hand2}: {card_value(hand1[i])} > {card_value(hand2[i])}")
                return 1
            elif card_value(hand1[i]) < card_value(hand2[i]):
                # print(f"Card value for {hand1} < {hand2}: {card_value(hand1[i])} < {card_value(hand2[i])}")
                return -1
            else:
                continue

    # print(f"Hands are identical: {hand1} = {hand2}")
    return 0

def get_list_of_random_hands(count: int, jokers=True):
    available_cards = "AKQJT98765432"
    if jokers:
        available_cards += "J"
    for _ in range(count):
        random_hand = "".join(random.sample(available_cards, 5))
        yield random_hand

def modify_with_jokers(hand: str) -> str:
    hand_as_list = list(hand)
    non_joker_indices = [i for i in range(len(hand)) if hand[i] != "J"]
    joker_amount = random.randint(1, len(non_joker_indices)-1)
    indices = random.sample(non_joker_indices, joker_amount)
    # print(f"{len(indices)} jokers")
    for index in indices:
        hand_as_list[index] = "J"
    return "".join(hand_as_list)

'''
for hand in get_list_of_random_hands(1000000, jokers=False):
    modified = modify_with_jokers(hand)
    if compare_hands(hand, modified) == 0:
        print(f"{hand} & {modified} got the same comparison")
        print(f"{hand} = {hand_type_value(hand)}")
        print(f"{modified} = {hand_type_value(modified)}")
        exit()
'''

hands_by_rank = sorted(hands_and_bids, key=functools.cmp_to_key(compare_hands))

print(f"\nBy rank:")
total_winnings = 0
for i in range(len(hands_by_rank)):
    total_winnings += (i+1) * hands_and_bids[hands_by_rank[i]]
    print(hands_by_rank[i])

print(f"\nTotal winnings:")
print(total_winnings)

