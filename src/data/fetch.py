# Imported Libraries (requests for HTTP requests, time for potential future use in rate limiting)
import requests, time

# Imported pandas for potential future use in data manipulation, and csv for writing to CSV files
import pandas as pd

# Function to fetch Pokemon stats from the PokeAPI
def get_pokemon_stats(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
    try: 
        # Added a 5-second timeout to handle potential network issues
        response = requests.get(url, timeout=5)

        # Check if the request was successful (status code 4xx or 5xx will raise an HTTPError)
        response.raise_for_status()  
        data = response.json()

        return{
            "name": data["name"],
            "hp" : data["stats"][0]["base_stat"],
            "attack" : data["stats"][1]["base_stat"],
            "defense" : data["stats"][2]["base_stat"],
            "special-attack" : data["stats"][3]["base_stat"],
            "special-defense" : data["stats"][4]["base_stat"],
            "speed" : data["stats"][5]["base_stat"],
            "type1" : data["types"][0]["type"]["name"],
            "type2" : data["types"][1]["type"]["name"] if len(data["types"])>1 else None
        }
    
    # Added specific exception handling for HTTP errors and general request exceptions to provide clearer error messages
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error fetching for {name}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network/Connection error for {name}: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error for {name}: {e}")


# Function to fetch stats for all Pokemon
def fetch_all_pokemon():
    # Fetch the list of all Pokemon from the PokeAPI (limit set to 1025 to include all known Pokemon)
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1025'
    try:
        response = requests.get(url, timeout=10)

        # Check for HTTP errors
        response.raise_for_status() 
        data = response.json()
        pokemon_list = data['results']
    except requests.exceptions.RequestException as e:
        print(f"Fatal Error: Failed to fetch initial Pokemon list: {e}")

        # Return an empty list if we can't fetch the initial list of Pokemon
        return []  

    all_pokemon_stats = []
    for pokemon in pokemon_list:
        stats = get_pokemon_stats(pokemon['name'])

        # Only append if stats were successfully fetched
        if stats is not None:  
            all_pokemon_stats.append(stats)

        # Sleep to avoid hitting API rate limits
        time.sleep(0.5)  
    
    return all_pokemon_stats
    
def save_to_csv(data, filename='data/raw/pokemon_stats.csv'):
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




