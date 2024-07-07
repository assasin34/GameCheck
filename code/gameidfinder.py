import difflib
import requests
import os
from time import sleep

url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
results = []
response = requests.get(url)
data = response.json()

def animate_print(text):    # Function to animate text
        for char in text:
            print(char, end='', flush=True)
            sleep(0.002)

# Parse the response data into a dictionary
game_data = {game['name'].lower(): game['appid'] for game in data['applist']['apps']}

# Check if the file with game names exists
if os.path.isfile('games.txt'):
    animate_print("The games.txt file exists. Reading game names...\n")
    with open('games.txt', 'r', encoding='utf-8') as file:
        game_names = file.read().lower().splitlines()
else:
    # Ask the user if the file is in a different path
    animate_print("Couldn't find games.txt file.\n")
    path_input = input("Does the txt file have a diffrent name or is in a different directory? (Y/N): ")
    if path_input.lower() == 'y':
        # Ask the user for the path to the file
        path = input("Enter the path to the games.txt file: ")
        # Check if the file exists at the specified path
        if os.path.isfile(path):
            animate_print("The file found at the specified path. Reading game names...\n")
            with open(path, 'r', encoding='utf-8') as file:
                game_names = file.read().lower().splitlines()
        else:
            # Ask the user for manual input of game names
            animate_print("The file was not found at the specified path. Please enter the game names manually.\n")
            game_names = input("Enter the game names (separated by commas): ").lower().split(",")
    else:
        # Ask the user for manual input of game names
        game_names = input("Enter the game names manually (separated by commas): ").lower().split(",")

for game_name in game_names:
    if game_name in game_data:
        appid = game_data[game_name]
        animate_print(f"\nThe appid for {game_name} is {appid}")
        results.append(f"https://store.steampowered.com/app/{appid}" + " - " + game_name + "\n")
    else:
        closest_match = difflib.get_close_matches(game_name, game_data.keys(), n=1)
        if closest_match:
            appid = game_data[closest_match[0]]
            animate_print(f"\n[{game_name}] not found in the database. Did you mean [{closest_match[0]}]?\n")
            verify_input = input("Is that the game you were looking for? (Y/N): ")
            if verify_input.lower() == 'y':
                animate_print(f"\nThe appid for {closest_match[0]} is {appid}")
                results.append(f"https://store.steampowered.com/app/{appid} - {closest_match[0]}\n")
        else:
            animate_print("Game name not found in the data.")

animate_print('\n\nWriting results to txt file...\n')
with open('links.txt', 'w', encoding='utf-8') as file:
    file.write("".join(results))
input("Press any key to exit...")