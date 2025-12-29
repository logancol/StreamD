import requests
import os
from datetime import datetime
import numpy as np
import json
from dotenv import load_dotenv

load_dotenv()



# loads all game id's for a given nba season

# load all ids for the regular season games for the past 25 years and join this with player games to exclude playoff, preseason games
def load_season_games(season):
    print(f'-- LOADING GAME IDS FOR SEASON: {season} --')
    url = 'https://v2.nba.api-sports.io/games'
    headers = {
        'x-apisports-key': os.getenv("FOOTBALL-API_KEY")
    }
    params = {
        'season': season
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    games = data['response']
    regular_season_games = []
    for game in games:
        if game['stage'] == 2:
            regular_season_games.append(game['id'])
    return regular_season_games

all_ids = []
for i in range(2000, 2025):
    year = load_season_games(i)
    for id in year:
        all_ids.append(id)
print(len(all_ids))
