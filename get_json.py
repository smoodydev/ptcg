import json
import requests

def retrieve_and_save_data(output_file):
    base_url = "https://api.pokemontcg.io/v2/cards/base2-"



    all_data = []

    # if response.status_code == 200:
    #     data = response.json()
    #     all_data.append(data)
    #     print(f"Data for Pokémon {number} retrieved successfully.")
    # else:
    #     print(f"Failed to retrieve data for Pokémon {number}. Status code: {response.status_code}")

    for number in range(1, 64):
        url = base_url + str(number)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            all_data.append(data)
            print(f"Data for Pokémon {number} retrieved successfully.")
        else:
            print(f"Failed to retrieve data for Pokémon {number}. Status code: {response.status_code}")

    with open(output_file, 'w') as file:
        json.dump(all_data, file)

    print(f"All data retrieved and saved to {output_file} successfully.")


# Example usage:
output_file = "pokemon_jungle.json"

retrieve_and_save_data(output_file)