import requests
import json

def todays_games():
    url = 'https://statsapi.web.nhl.com/api/v1/schedule'
    response = requests.get(url)
    games = response.json()
    return games['dates'][0]['games']