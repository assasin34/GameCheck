import requests
import webbrowser
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from time import sleep
from threading import Thread

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
| Inputing lots of links might lag the   |
| website for some time so just patient  |
\________________________________________/

""")

def animate_print(text):    # Function to animate text
        for char in text:
            print(char, end='', flush=True)
            sleep(0.01)

@app.route('/', methods=['GET', 'POST'])
def index():
    image_urls = []
    if request.method == 'POST':
        steam_urls = request.form['steam_urls'].split(',')
        for url in steam_urls:
            image_url = get_game_image(url.strip())
            if image_url:
                image_urls.append({'url': image_url, 'steam_url': url.strip()})
    return render_template('indexmanual.html', image_urls=image_urls)

@app.route('/get_description')
def get_description():
    url = request.args.get('url')
    description = get_game_description(url)
    return description if description else 'Description not found'

if __name__ == '__main__':
    disclaimer()
    sleep(2)
    thread = Thread(target=open_the_website)
    thread.start()
    app.run()