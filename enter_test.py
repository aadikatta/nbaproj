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

#player1_name = input('What is the name of the first player?\n')
#player2_name = input('What is the name of the second player?\n')


#testing purposes
player1_name = 'Austin Reaves'
player2_name = 'Anthony Edwards'



player1 = [player for player in player_dict if player['full_name'] == player1_name][0]
player1_id = player1['id']
player2 = [player for player in player_dict if player['full_name'] == player2_name][0]
player2_id = player2['id']

player1_games = playergamelog.PlayerGameLog(player_id=player1_id, season=SeasonAll.previous_season).get_normalized_dict()
player1_games_dict = player1_games['PlayerGameLog']
player1_print = [game["Game_ID"] for game in player1_games_dict]

player2_games = playergamelog.PlayerGameLog(player_id=player2_id, season=SeasonAll.previous_season).get_normalized_dict()
player2_games_dict = player2_games['PlayerGameLog']
player2_print = [game["Game_ID"] for game in player2_games_dict]
player2_full = [game for game in player2_games_dict]

player2vsplayer1_dict = [game_id for game_id in player1_print if game_id in player2_print]

player1vs_dict = [game for game in player1_games_dict if game['Game_ID'] in player2vsplayer1_dict]
player2vs_dict = [game for game in player2_games_dict if game['Game_ID'] in player2vsplayer1_dict]

'''print(player1_print)
print('\n\n\n')'''

print(player2vsplayer1_dict)

print('\n\n\n')

print('----------------' + player1_name + '----------------')
print([(game['PTS'], game['FG_PCT']) for game in player1vs_dict])

print('\n\n')

print('----------------' + player2_name + '----------------')
print([(game['PTS'], game['FG_PCT']) for game in player2vs_dict])