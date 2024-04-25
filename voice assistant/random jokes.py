import requests
from bs4 import BeautifulSoup
import random

def get_random_joke_html():
    url = 'https://randstuff.ru/joke/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    joke_divs = soup.find_all('div', class_='text')
    if joke_divs:
        return random.choice(joke_divs).prettify()
    else:
        return "Не удалось получить шутку. Попробуйте позже."

if __name__ == "__main__":
    joke_html = get_random_joke_html()
    print(joke_html)
