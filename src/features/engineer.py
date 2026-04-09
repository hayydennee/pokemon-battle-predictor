# Import Pandas
import pandas as pd

# Import Pokemon class from generate_battle.py
from src.data.generate_battle import Pokemon

# Import the save_to_csv function from the utils module
from src.utils import save_to_csv

# Import type chart
from src.features.type_chart import build_type_chart
type_chart = build_type_chart()

# Read pokemon_stats CSV into a DataFrame
df_pokemon = pd.read_csv('data/raw/pokemon_stats.csv')
pokemon_lookup = df_pokemon.set_index('name').to_dict(orient='index')

# Load battles CSV into a DataFrame
df_battles = pd.read_csv('data/battles/battles.csv')

# Loop through each battle row and create a new DataFrame with the relevant stats
engineer_data = []
for _, row in df_battles.iterrows():
    attacker = pokemon_lookup[row['attacker']]
    defender = pokemon_lookup[row['defender']]
    type_a_vs_b = type_chart[attacker['type1']][defender['type1']]
    type_b_vs_a = type_chart[defender['type1']][attacker['type1']]
    if pd.notna(defender['type2']):
        type_a_vs_b *= type_chart[attacker['type1']][defender['type2']]
    if pd.notna(attacker['type2']):
        type_b_vs_a *= type_chart[defender['type1']][attacker['type2']]
    if row['attacker'] == row['winner']:
        label = 1
    else: 
        label = 0
    engineer_data.append({
        'hp_diff': attacker['hp'] - defender['hp'],
        'attack_diff': attacker['attack'] - defender['attack'],
        'defense_diff': attacker['defense'] - defender['defense'],
        'speed_diff': attacker['speed'] - defender['speed'],
        'sp_attack_diff': attacker['special-attack'] - defender['special-attack'],
        'sp_defense_diff': attacker['special-defense'] - defender['special-defense'],
        'type_a_vs_b': type_a_vs_b,
        'type_b_vs_a': type_b_vs_a,
        'label': label
    })

# Save engineered data to CSV
save_to_csv(engineer_data, 'data/processed/features.csv')