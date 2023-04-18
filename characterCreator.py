import csv
import random
import os.path

file_exists = os.path.isfile('characters.csv')
mode = 'a' if file_exists else 'w'

# Define the list of races, classes, and alignments
RACES = ['Human', 'Elf', 'Dwarf', 'Halfling', 'Dragonborn', 'Half-Elf', 'Gnome', 'Tiefling', 'Half-Orc']
CLASSES = {
    'Fighter': ['Strength', 'Constitution'],
    'Wizard': ['Intelligence', 'Wisdom'],
    'Rogue': ['Dexterity', 'Charisma'],
    'Cleric': ['Wisdom', 'Strength'],
    'Bard': ['Charisma', 'Dexterity'],
    'Ranger': ['Dexterity', 'Wisdom'],
    'Sorcerer': ['Charisma', 'Constitution'],
    'Paladin': ['Strength', 'Charisma'],
    'Monk': ['Dexterity', 'Wisdom'],
    'Barbarian': ['Strength', 'Constitution']
}
ALIGNMENTS = ['Lawful Good', 'Neutral Good', 'Chaotic Good', 'Lawful Neutral', 'True Neutral', 'Chaotic Neutral', 'Lawful Evil', 'Neutral Evil', 'Chaotic Evil']

# Define the point buy cost for each stat value
# POINT_BUY_COST = [0, 2, 5, 9, 15, 20, 27]
POINT_BUY_COST = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8]

def roll_stats():
    """Roll 4d6, drop the lowest roll, and reroll 1s"""
    stats = {}
    for stat_name in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']:
        rolls = sorted([random.randint(1, 6) for _ in range(4)])
        if rolls[0] == 1:
            rolls = [random.randint(2, 6) if roll == 1 else roll for roll in rolls]
        stat_value = sum(rolls[1:])
        stats[stat_name] = stat_value
    return stats

STAT_RANGE = range(8, 17)

def point_buy_stats(points = 27):
    # Set the point costs for each ability score
    point_costs = {
        8: 0,
        9: 1,
        10: 2,
        11: 3,
        12: 4,
        13: 5,
        14: 7,
        15: 9
    }
    
    # Set the maximum number of points that can be spent
    max_points = 27
    
    # Initialize an empty dictionary to store the ability scores
    stats = {}
    
    # Loop through each ability score and randomly generate a score
    for ability in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']:
        valid_score = False
        while not valid_score:
            score = random.randint(8, 15)
            if score <= (15 - max_points):
                valid_score = True
                stats[ability] = score
                max_points -= point_costs[score]

    return stats

def generate_characters(num_characters=1, method_ratio=[1]):
    """Generate a list of characters using the specified method ratio"""
    methods = {
        'Dice Rolling': lambda: [roll_stats()],
        'Point Buy': lambda: point_buy_stats(27)
    }
    characters = []
    method_count = {'Dice Rolling': 0, 'Point Buy': 0}
    for i in range(num_characters):
        method = random.choices(list(methods.keys()), weights=method_ratio)[0]
        method_count[method] += 1
        stats = methods[method]()
        print(stats)
        # character_class = random.choice(list(CLASSES.keys()))
        # top_stat, second_stat = CLASSES[character_class]
        # # Assign the class bonuses to the top and second stats
        # top_stat_index = CLASSES.index(top_stat)
        # second_stat_index = CLASSES.index(second_stat)
        # stats[top_stat_index] += 2
        # stats[second_stat_index] += 1
        character = {
            'race': random.choice(RACES),
            # 'class': character_class,
            'align': random.choice(ALIGNMENTS),
            'str': stats[0]["Strength"],
            'dex': stats[0]["Dexterity"],
            'con': stats[0]["Constitution"],
            'int': stats[0]["Intelligence"],
            'wis': stats[0]["Wisdom"],
            'cha': stats[0]["Charisma"]
        }
        characters.append(character)

    print(f"Generated {num_characters} characters using the following methods: {method_count}")
    return characters


characters = generate_characters(num_characters=1000, method_ratio=[1, 0])

with open('Data/data.csv', mode='w', newline='') as csv_file:
    fieldnames = ['race', 'align', 'str', 'dex', 'con', 'int', 'wis', 'cha']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for character in characters:
        writer.writerow(character)
print("Characters saved to characters.csv")
