import json
import requests
from speak import speak

def say_chuck_norris_joke():
    
    raw_web_data = requests.get('https://api.chucknorris.io/jokes/random')
    json_web_data = json.loads(raw_web_data.text)
    chuck_norris_joke = json_web_data['value']

    split_joke = chuck_norris_joke.split(' ')

    # Full joke needs to be broken down
    #   into pieces or quality drops
    chunk_size = 8
    num_chunks = len(split_joke) / float(chunk_size)
    for i in range(int(num_chunks)+1):
        speak(" ".join(split_joke[i * chunk_size : (i + 1) * chunk_size]),
              speed=110)

if __name__ == '__main__':
    say_chuck_norris_joke()
