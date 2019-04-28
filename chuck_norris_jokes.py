import json
import requests
import random
from speak import speak
from banned_words_fb import bad_words

BANNED_LIST = ['explicit', 'political', 'religion', 'history']  # (note that history had Nagasaki jokes....)]

def say_chuck_norris_joke():
    raw_category_values = requests.get('https://api.chucknorris.io/jokes/categories')
    json_web_data = json.loads(raw_category_values.text)
    categories = [cat for cat in json_web_data if cat not in BANNED_LIST]
    selected = random.choice(categories)

    raw_web_data = requests.get('https://api.chucknorris.io/jokes/random?category={category}'.format(category=selected))
    json_web_data = json.loads(raw_web_data.text)
    chuck_norris_joke = json_web_data['value']

    has_bad_word = False
    swears = []
    chuck_norris_joke_lwr = chuck_norris_joke.lower()
    for bad_word in bad_words:
        if chuck_norris_joke_lwr.find(bad_word) > 0:
            has_bad_word = True
            swears.append(bad_word)

    if has_bad_word:
        print('....Actually, this joke has a swear, let me grab a different one....')
        say_chuck_norris_joke()
    else:
        print("I love parties!! I have a joke...   {}".format(chuck_norris_joke))
        speak(chuck_norris_joke)

if __name__ == '__main__':
    say_chuck_norris_joke()
