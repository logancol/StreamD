import psycopg2
from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.endpoints import playerindex
import time
import re
import pandas as pd

conn = psycopg2.connect(
    database="streamd",
    user="docker",
    password="docker",
    port=5431
)
cur = conn.cursor()

team_abbreviations = [
    "ATL", "BOS", "BRK", "CHI", "CHO", "CLE", "DAL", "DEN",
    "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA",
    "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHX",
    "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
]

all_teams = teams._get_teams()
for team in all_teams:
    id = team['id']
    full_name = team['full_name']
    abbreviation = team['abbreviation']
    nickname = team['nickname']
    city = team['city']
    cur.execute("INSERT INTO Team (team_id, team_full_name, team_abbreviation, team_nickname, team_city) VALUES (%s, %s, %s, %s, %s)", (id, full_name, abbreviation, nickname, city))
conn.commit()