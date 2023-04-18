import csv
import random
import os.path

file_exists = os.path.isfile('characters.csv')
mode = 'a' if file_exists else 'w'

# Define the list of races, classes, and alignments
RACES = ['Human', 'Elf', 'Dwarf', 'Halfling']
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
    rolls = sorted([random.randint(1, 6) for _ in range(4)])
    if rolls[0] == 1:
        rolls = [random.randint(2, 6) if roll == 1 else roll for roll in rolls]
    return sum(rolls[1:])

def point_buy_stats(points):
    stats = [8, 8, 8, 8, 8, 8]
    points = int(points)
    while points > 0:
        stat = random.randint(0, 5)
        if stats[stat] >= 15:
            continue  # skip if the stat is already at the maximum value
        else:
            cost = POINT_BUY_COST[stats[stat] + 1] - POINT_BUY_COST[stats[stat]]
        if cost <= points:
            stats[stat] += 1
            points -= cost
    return stats

def generate_characters(num_characters=1, method_ratio=[1]):
    """Generate a list of characters using the specified method ratio"""
    methods = {
        'Dice Rolling': lambda: [roll_stats() for _ in range(6)],
        'Point Buy': lambda: point_buy_stats(27)
    }
    characters = []
    method_count = {'Dice Rolling': 0, 'Point Buy': 0}
    for i in range(num_characters):
        method = random.choices(list(methods.keys()), weights=method_ratio)[0]
        method_count[method] += 1
        stats = methods[method]()
        print(stats)
        character_class = random.choice(list(CLASSES.keys()))
        # top_stat, second_stat = CLASSES[character_class]
        # Assign the class bonuses to the top and second stats
        # top_stat_index = CLASSES.index(top_stat)
        # second_stat_index = CLASSES.index(second_stat)
        # stats[top_stat_index] += 2
        # stats[second_stat_index] += 1
        character = {
            'race': random.choice(RACES),
            'class': character_class,
            'alignment': random.choice(ALIGNMENTS),
            'strength': stats[0],
            'dexterity': stats[1],
            'constitution': stats[2],
            'intelligence': stats[3],
            'wisdom': stats[4],
            'charisma': stats[5]
        }
        characters.append(character)

    print(f"Generated {num_characters} characters using the following methods: {method_count}")
    return characters


# Generate 10 characters with a ratio of 2 Point Buy to 1 Dice Rolling, and save the characters to a CSV file
characters = generate_characters(num_characters=4, method_ratio=[2, 1])

with open('Data/data.csv', mode=mode, newline='') as csv_file:
    fieldnames = ['race', 'class', 'alignment', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for character in characters:
        writer.writerow(character)
print("Characters saved to characters.csv")
