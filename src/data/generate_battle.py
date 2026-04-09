# Import pandas for data manipulation
import pandas as pd

# Generate all possible battles between Pokemon (no repeats)
from itertools import combinations

# Import the simulate function from the simulate module
from src.data.simulate import simulate

# Import the save_to_csv function from the utils module
from src.utils import save_to_csv

# Import type chart
from src.features.type_chart import build_type_chart

type_chart = build_type_chart()

# Create Pokemon class to hold stats
class Pokemon:
    def __init__(self, row):
        self.name = row['name']
        self.type1 = row['type1']
        self.type2 = row['type2'] if pd.notna(row['type2']) else None
        self.base_hp = int(row['hp'])
        self.hp = self.base_hp
        self.attack = int(row['attack'])
        self.defense = int(row['defense'])
        self.special_attack = int(row['special-attack'])
        self.special_defense = int(row['special-defense'])
        self.speed = int(row['speed'])

# Load Pokemon data 
df = pd.read_csv('data/raw/pokemon_stats.csv')
all_pokemon = []
for _, row in df.iterrows():
    all_pokemon.append(Pokemon(row))

# Loop through combinations
battles = []
all_pairs = combinations(all_pokemon, 2)
for attacking, defending in all_pairs:
    attacking.hp = attacking.base_hp
    defending.hp = defending.base_hp
    winner = simulate(attacking, defending, type_chart)
    battles.append({
        'attacker': attacking.name,
        'defender': defending.name,
        'winner': winner.name
    })

# Save battles to CSV
if __name__ == "__main__":
    print("Saving battles to CSV...")
    save_to_csv(battles, 'data/battles/battles.csv')