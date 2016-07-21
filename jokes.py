from speak import speak
import unirest

# These code snippets use an open-source library. http://unirest.io/python
response = unirest.get("https://webknox-jokes.p.mashape.com/jokes/search?keywords=mamma&minRating=5&numJokes=3",
  headers={
    "X-Mashape-Key": "FCSgB8Lb9GmshGNMw344E370qHhGp1c0Iyjjsn7MUCLyH8b95Z",
    "Accept": "application/json"
  }
)

jokes = [joke['joke'] for joke in response._body]
for joke in jokes:
    speak(joke)
