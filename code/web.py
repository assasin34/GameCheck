import os
import sys
import requests
import webbrowser
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from threading import Thread
from time import sleep

app = Flask(__name__)

def get_game_image(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    image_element = soup.find('img', class_='game_header_image_full')
    if image_element:
        return image_element['src']
    return None

def get_game_description(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    description_element = soup.find('div', id='game_area_description')
    if description_element:
        # Find all image tags within the description
        image_tags = description_element.find_all('img')
        
        # Append image tags with their src attribute to the description content
        for img_tag in image_tags:
            img_src = img_tag.get('src')
            img_tag['src'] = img_src
            description_element.append(img_tag)
        
        # Get the modified description HTML with images
        description = str(description_element)
        
        return description
    return None

def open_the_website():
    sleep(1)
    webbrowser.open_new('http://127.0.0.1:5000/')

def disclaimer():
    animate_print("""
 ________________________________________ 
/                                        \ 
|           *** DISCLAIMER ***           |
| Website might take a long time to load |
| depending on how many games are in TXT |
\________________________________________/

""")

def animate_print(text):    # Function to animate text
        for char in text:
            print(char, end='', flush=True)
            sleep(0.01)

@app.route('/', methods=['GET', 'POST'])
def index():
    image_urls = []
    
    with open('links.txt', 'r', encoding='utf-8') as file:
        for line in file:
            url = line.split(' ')[0]  # Extract the URL part before the space
            image_url = get_game_image(url.strip())
            if image_url:
                image_urls.append({'url': image_url, 'steam_url': url.strip()})
    return render_template('index.html', image_urls=image_urls)

@app.route('/get_description')
def get_description():
    url = request.args.get('url')
    description = get_game_description(url)
    return description if description else 'Description not found'

if __name__ == '__main__':
    if not os.path.exists('links.txt'):
        animate_print('links.txt file does not exist. Please create one or use the manual version\n')
        input("Press any key to exit...")
        sys.exit(1)
    disclaimer()
    sleep(2)
    thread = Thread(target=open_the_website)
    thread.start()
    app.run()