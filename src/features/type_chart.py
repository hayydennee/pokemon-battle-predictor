# Imported Libraries (requests for HTTP requests, time for potential future use in rate limiting)
import requests, time
    
# Imported pandas for potential future use in data manipulation, and csv for writing to CSV files
import pandas as pd

# Function to build the type chart by fetching data for all types from the PokeAPI
def build_type_chart():
    url = 'https://pokeapi.co/api/v2/type?limit=21'
    try:
        # Added a 5-second timeout to handle potential network issues
        response = requests.get(url, timeout=5)

        # Check if the request was successful (status code 4xx or 5xx will raise an HTTPError)
        response.raise_for_status()
        data = response.json()
        types = [t["name"] for t in data['results']]
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error fetching type list: {e}")

        # Return an empty list if we can't fetch the initial list of Pokemon
        return []  
    
    # Initialize every matchup to be neutral (1x damage) before updating with actual type effectiveness data
    chart = {}
    for attacking_type in types:
        chart[attacking_type] = {}
        for defending_type in types:
            chart[attacking_type][defending_type] = 1.0

    # Fetch the type effectiveness data for each type and update the chart accordingly
    for attacking_type in types:
        url = f'https://pokeapi.co/api/v2/type/{attacking_type}'
        try:
            response = requests.get(url, timeout=5)

            # Check if the request was successful (status code 4xx or 5xx will raise an HTTPError)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error fetching type data for {attacking_type}: {e}")
            
        relations = data["damage_relations"]

        # Overwrite double damage
        for t in relations["double_damage_to"]:
            chart[attacking_type][t["name"]] = 2.0
        
        # Overwrite half damage
        for t in relations["half_damage_to"]:
            chart[attacking_type][t["name"]] = 0.5
        
        # Overwrite no damage
        for t in relations["no_damage_to"]:
            chart[attacking_type][t["name"]] = 0.0
        
        # Sleep to avoid hitting API rate limitss
        time.sleep(0.3)  
    return chart

def save_to_csv(data, filename='data/raw/type_chart.csv'):
    # Safety check to ensure data is not empty before attempting to write to CSV
    if not data:
        print("No data to save. CSV file will not be created.")
        return
    
    # Convert the list of dictionaries to a DataFrame for easier CSV writing
    df = pd.DataFrame(data)

    # Save that DataFrame to a CSV file, including error handling for potential file I/O issues
    try:
        df.to_csv(filename, index=False)
    except IOError as e:
        print(f"File I/O error while saving to {filename}: {e}")

    print(f"Data successfully saved to {filename}")

# Main execution block to fetch Pokemon data and save it to a CSV file
print("Saving to CSV...")
type_chart = build_type_chart()
save_to_csv(type_chart)



            
