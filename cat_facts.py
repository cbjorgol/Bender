import json
import requests
from speak import speak

def say_cat_fact():
    
    raw_web_data = requests.get('http://catfacts-api.appspot.com/api/facts')
    json_web_data = json.loads(raw_web_data.text)
    print json_web_data
    chuck_norris_joke = json_web_data['facts'][0]
    split_fact = chuck_norris_joke.split(' ')

    # Full joke needs to be broken down
    #   into pieces or quality drops
    chunk_size = 8
    num_chunks = len(split_fact) / float(chunk_size)
    for i in range(int(num_chunks)+1):
        speak(" ".join(split_fact[i * chunk_size : (i + 1) * chunk_size]),
              speed=120,
              language='en-us+f2',
              pitch_adj=10)

if __name__ == '__main__':
    say_cat_fact()
