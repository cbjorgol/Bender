import json
import requests
from speak import speak

def say_chuck_norris_joke():
    
    raw_web_data = requests.get('https://api.chucknorris.io/jokes/random')
    json_web_data = json.loads(raw_web_data.text)
    chuck_norris_joke = json_web_data['value']
    print(chuck_norris_joke)
    speak(chuck_norris_joke)

if __name__ == '__main__':
    say_chuck_norris_joke()
