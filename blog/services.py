import os
import requests


def get_games():
    url = 'https://boardgamegeek.com/xmlapi2/hot?type=boardgame'
    r = requests.get(url)
    boardgames = r.json()
    games_list = []
    for game in range(len(boardgames['games'])):
        games_list.append(boardgames['games'][game])
    return games_list