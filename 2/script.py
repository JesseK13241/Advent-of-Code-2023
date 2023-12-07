'''
The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
'''

max_amounts = {"red": 12, "green": 13, "blue": 14}
min_amounts = {"red": 0, "green": 0, "blue": 0}

def set_possible(set: str) -> bool:
    # 3 blue, 4 red
    cube_amounts_and_colors = set.split(",")
    for c in cube_amounts_and_colors:
        amount, color = c.strip().split(" ")
        max_amount = max_amounts[color]
        if int(amount) > max_amount:
            print(f"Too many {color} cubes: ({amount} > {max_amount})\n")
            return False
    return True

def game_possible(game: str) -> bool:
    #  3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    sets = game.split(";")
    for set in sets:
        if not set_possible(set):
            return False
    return True

def get_game_power(game: str) -> int:
    # # The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. 
    print()
    print(game)
    sets = game.split(";")
    game_min_amounts = dict(min_amounts)
    for set in sets:
        cube_amounts_and_colors = set.split(",")
        for c in cube_amounts_and_colors:
            amount, color = c.strip().split(" ")
            if int(amount) > game_min_amounts[color]:
                game_min_amounts[color] = int(amount)

    product = 1
    print(game_min_amounts)
    for min_amount in game_min_amounts:
        product *= game_min_amounts[min_amount]
    return product

with open("input") as f:
    
    lines = f.read().splitlines()
    total = 0

    ''' # part 1
    for line in lines:
        print(line)
        game_id, game = line.split(":")
        game_id = int(game_id.split()[-1])
        if game_possible(game):
            total += game_id
    print(f"\nSum of possible games: {total}")

    ''' # part 2
    for line in lines:
        game_id, game = line.split(":")
        game_power = get_game_power(game)
        total += game_power
        print(f"The power for game {game_id} is {game_power}")

    print(f"\nTotal sum of the game powers: {total}")