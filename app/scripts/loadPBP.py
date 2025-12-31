import psycopg2
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.endpoints import playbyplayv3
import isodate
import time
import re
import pandas as pd

# Getting orlando magic team id

nba_teams = teams.get_teams()
magic = [team for team in nba_teams if team['abbreviation'] == 'ORL'][0]
magic_id = magic['id']
print(f'magic id: {magic_id}')

# Getting games from this season (regular season games from this year)

gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=magic_id,
                            season_nullable=Season.default,
                            season_type_nullable=SeasonType.regular)  
games_dict = gamefinder.get_normalized_dict()
games = games_dict['LeagueGameFinderResults']

# Get play by play from found games 

dfs = []

for game in games:
    dfs.append(playbyplayv3.PlayByPlayV3(game_id = game['GAME_ID']).get_data_frames()[0])
    time.sleep(2) # avoid hitting rate limit

# connect to database

conn = psycopg2.connect(
    database="streamd",
    user="docker",
    password="docker",
    port=5431
)

# Open cursor to perform database operations
cur = conn.cursor()

# final_df contains all of the playbyplay info for the specified timeframe that we need to go through

# https://github.com/swar/nba_api/blob/master/docs/examples/PlayByPlay.ipynb sourced for play by play endpoint usage

# -- IN THE FUTURE, SET UP SUPPORT FOR SHOT CHART DETAIL ENDPOINT WHICH WILL GIVE COORDINATES AND MORE ACCURATE SHOT LOCATION INFORMATION



final_df = pd.concat(dfs, ignore_index=True)
game_teams = (
    final_df[['gameId', 'location', 'teamId']]
    .drop_duplicates()
    .pivot(index='game_id', columns='location', values='teamId')
    .rename(columns={'h': 'home_team_id', 'v': 'visiting_team_id'})
)
final_df = final_df.merge(game_teams, on='game_id', how='left')
for index, row in final_df.iterrows():
    # retooling with v3 endpoint its way better
    if row['isFieldGoal'] == 1:
        game_id = row['gameId']
        event_num = row['actionNumber']
        event_type = row['actionType']
        event_subtype = row['subType']
        season = row['season'] # must add manually
        season_type = row['season_type'] # must add manually
        period = row['period']
        posession_team_id = row['teamId']
        primary_player_id = row['personId']
        home_team_id = row['home_team_id']
        away_team_id = row['visiting_team_id']
        

        








#cur.execute("INSERT INTO Games (game_id, season) VALUES (%s, %s)", (1929, 20002))
#cur.execute("SELECT * FROM Games")
#rows = cur.fetchall()
#conn.commit()
#print(rows)

# Query the databse
# docker exec -it streamd_db psql -U docker -d streamd lets you work with the db from command line