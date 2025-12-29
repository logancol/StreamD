import requests
import pandas as pd
from scipy import stats
import os
import pytz
from datetime import datetime
import numpy as np
import json
from dotenv import load_dotenv

load_dotenv()

# for initial load of nba player data

# getting players on a team and then getting their individual statistical info, this probably a good way to keep up on rostered players?
# will cross check with other sources for accuracy

def get_player_ids_team(id):
    url = "https://v2.nba.api-sports.io/players"
    headers = {
        'x-apisports-key': os.getenv("FOOTBALL-API_KEY")
    }
    params = {
        'season': '2025', # this should reference a global variable down the road
        'team': id
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    player_data = data['response']
    ids = []
    for player in player_data:
        ids.append(player['id'])
    return ids

def get_active_player_ids():
    all_ids = []
    for team in range(1, 2): # only changes upon league expansion
        team_ids = get_player_ids_team(team)
        for id in team_ids:
            all_ids.append(id)
        print(f'--- Loaded Ids From Team ID: {team} ---')
    return all_ids

def get_all_player_stats_proto():
    #ids = get_active_player_ids()
    #test_id = ids[0] # just messing for now
    test_id = 265
    url = "https://v2.nba.api-sports.io/players/statistics"
    headers = {
        'x-apisports-key': os.getenv("FOOTBALL-API_KEY")
    }
    params = {
        'season': '2023',
        'id': test_id
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    game_data = data['response']
    games = []
    for game in game_data:
        game_struc = {
            'points': game['points'],
            'minutes': game['min']
        }
        games.append(game_struc)
    for i, game in enumerate(games):
        print(f'--- GAME: {i + 1} {game} ---')

def get_all_player_stats(season = 2025):
    ids = get_active_player_ids
    test_id = ids[0]
    url = 'https://v2.nba.api-sports.io/games'
    headers = {
        'x-apisports-key': os.getenv("FOOTBALL-API_KEY")
    }
    params = {
        'season': season,
        'team': test_id
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    game_data = data['response']
    games = []
    
    for game in game_data:
        univ_date = game['date']['start']
        utc_dt = datetime.strptime(univ_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        utc_dt = utc_dt.replace(tzinfo=pytz.UTC)
        pacific = pytz.timezone("US/Pacific")
        pt_dt = utc_dt.astimezone(pacific)

        game_struc = {
            'date': pt_dt.strftime("%Y-%m-%d %I:%M %p %Z"),
            'visiting team': game['teams']['visitors']['name'],
            'stage': game['stage']
        }
        games.append(game_struc)
    for i, game in enumerate(games):
        print(f'--- GAME: {i + 1} {game} ---')

def get_game():
    url = 'https://v2.nba.api-sports.io/games'
    headers = {
        'x-apisports-key': os.getenv("FOOTBALL-API_KEY")
    }
    params = {
        'season': 2025,
        'date': '2025-12-23'
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(data)

def get_banchero():
    url = 'https://v2.nba.api-sports.io/players/statistics'
    headers = {
        'x-apisports-key': os.getenv("FOOTBALL-API_KEY")
    }
    params = {
        'id': 3414,
        'game': 15926,
        'season': 2025
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(data)

# paolo id is 3414
get_banchero()