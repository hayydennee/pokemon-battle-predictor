# Imported Libraries (requests for HTTP requests, time for potential future use in rate limiting)
import requests, time

# Function to fetch Pokemon stats from the PokeAPI
def get_pokemon_stats(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
    response = requests.get(url)
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

def fetch_all_pokemon():
    
# Example usage of the function to fetch stats for Charizard and Pikachu
print(get_pokemon_stats("charizard"))
print(get_pokemon_stats("pikachu"))  # only one type - tests your type2 logic