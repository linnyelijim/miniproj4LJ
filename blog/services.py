import os
import requests


def get_games():
    url = 'https://boardgamegeek.com/xmlapi2/thing?type=boardgame'
    r = requests.get(url, headers={'Authorization':'Bearer %s' % 'access_token'})
    games = r.json()
    games_list = []
    for i in range(len(games['games'])):
        games_list.append(games['games'][i])
    return games_list