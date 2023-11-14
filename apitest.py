from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
import pandas as pd

player_dict = players.get_players()
teams_dict = teams.get_teams()


# Use ternary operator or write function 
# Names are case sensitive
#list comprehension: Useful for sorting through a dictionary
bron = [player for player in player_dict if player['full_name'] == 'LeBron James'][0]
bron_id = bron['id']
steph = [player for player in player_dict if player['full_name'] == 'Stephen Curry'][0]
steph_id = steph['id']

bron_games = playergamelog.PlayerGameLog(player_id=bron_id, season=SeasonAll.previous_season).get_normalized_dict()
bron_games_dict = bron_games['PlayerGameLog']
bron_print = [game["GAME_DATE"] for game in bron_games_dict]

steph_games = playergamelog.PlayerGameLog(player_id=steph_id, season=SeasonAll.previous_season).get_normalized_dict()
steph_games_dict = steph_games['PlayerGameLog']
steph_print = [game["GAME_DATE"] for game in steph_games_dict]
steph_full = [game for game in steph_games_dict]

stephvsbron_dict = [date for date in steph_print if date in bron_print]

'''print(bron_print)
print('\n\n\n')
print(steph_full)'''

print(stephvsbron_dict)



