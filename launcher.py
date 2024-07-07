import os
import subprocess
from time import sleep

web_path = './code/web.py'
webmanual_path = './code/webmanual.py'
gameid_path = './code/gameidfinder.py'

def clear_terminal(): #Clears the terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_print(text):    # Function to animate text
        for char in text:
            print(char, end='', flush=True)
            sleep(0.001)

def launcher():

    animate_print(f"""
   ____                       ____ _               _    
  / ___| __ _ _ __ ___   ___ / ___| |__   ___  ___| | __
 | |  _ / _` | '_ ` _ \ / _ \ |   | '_ \ / _ \/ __| |/ /
 | |_| | (_| | | | | | |  __/ |___| | | |  __/ (__|   < 
  \____|\__,_|_| |_| |_|\___|\____|_| |_|\___|\___|_|\_\ 
                                                           

Welcome!
Start by choosing the program you want to open:
      
1. Web application for displaying your games in a grid 
   (Requires links to the Steam store. Manual input is possible but links.txt file is recommended.)
      
2. GameIdFinder for creating a TXT file containing links to the Steam store 
   using only the names of the games 
   (Put the game names into games.txt file or input manually)
    """)


    question = input("\nEnter 1 or 2: ")

    if question == "1":
        clear_terminal()
        option = input("""What version would you like to use?
1.Txt file
2.Manual input
                       
Enter 1 or 2: """)
        if option == "1":
            clear_terminal()
            subprocess.call(['python', web_path])
        elif option == "2":
            clear_terminal()
            subprocess.call(['python', webmanual_path])
        else:
            print("Invalid input. Please enter 1 or 2.")
    elif question == "2":
        clear_terminal()
        subprocess.call(['python', gameid_path])
    else:
        print("Invalid input. Please enter 1 or 2.")


if __name__ == '__main__':
    launcher()