from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
import pandas as pd
import numpy as np

player_dict = players.get_players()
teams_dict = teams.get_teams()


# Use ternary operator or write function 
# Names are case sensitive
#list comprehension: Useful for sorting through a dictionary

#player1_name = input('What is the name of the first player?\n')
#player2_name = input('What is the name of the second player?\n')


#testing purposes
#Spelling must be correct
player1_name = 'Russell Westbrook'
player2_name = "Kevin Durant"

#Will return the stats of two players that played in games where the other player played in both of their careers
#Works for players that played on the same team or against each other

player1 = [player for player in player_dict if player['full_name'] == player1_name][0]
player1_id = player1['id']
player2 = [player for player in player_dict if player['full_name'] == player2_name][0]
player2_id = player2['id']

#change SeasonAll."previous_season" to retrieve seasons other than that one
#eventually should be able to take from all past and current seasons (with the ability to be changed upon input?)
player1_games = playergamelog.PlayerGameLog(player_id=player1_id, season=SeasonAll.all).get_normalized_dict()
player1_games_dict = player1_games['PlayerGameLog']
player1_print = [game["Game_ID"] for game in player1_games_dict]

player2_games = playergamelog.PlayerGameLog(player_id=player2_id, season=SeasonAll.all).get_normalized_dict()
player2_games_dict = player2_games['PlayerGameLog']
player2_print = [game["Game_ID"] for game in player2_games_dict]
player2_full = [game for game in player2_games_dict]

player2vsplayer1_dict = [game_id for game_id in player1_print if game_id in player2_print]

player1vs_dict = [game for game in player1_games_dict if game['Game_ID'] in player2vsplayer1_dict]
player2vs_dict = [game for game in player2_games_dict if game['Game_ID'] in player2vsplayer1_dict]

'''print(player1_games_dict)
print('\n\n\n')'''

#print(player2vsplayer1_dict)

print('\n\n\n')

print('----------------' + player1_name + '----------------')
print([(game['PTS'], game['FG_PCT'], game['PLUS_MINUS']) for game in player1vs_dict])

#average calculations can be done here once data is retrieved at the top
count = 0                                                                                       #avg points calculation
points = 0
for i in [(game['PTS']) for game in player1vs_dict]:
    count+=1
    points+=i

player1_points_avg = round(points/count, 2)

print('\n\n')

print('----------------' + player2_name + '----------------')
print([(game['PTS'], game['FG_PCT'], game['PLUS_MINUS']) for game in player2vs_dict])

#average calculations can be done here once data is retrieved at the top
count = 0
points = 0
for i in [(game['PTS']) for game in player2vs_dict]:
    count+=1
    points+=i

player2_points_avg = round(points/count, 2)


print('\n\n\n')
print(player1_name + ' Points Average: ' + str(player1_points_avg))
avg_pm_arr = np.mean([(game['PLUS_MINUS']) for game in player1vs_dict])                         #avg plus minus calculation
print(player1_name + ' Average Plus/Minus: ' + str(round(avg_pm_arr, 2)))
print('\n\n\n')
print(player2_name + ' Points Average: ' + str(player2_points_avg))
avg_pm_arr = np.mean([(game['PLUS_MINUS']) for game in player2vs_dict])
print(player2_name + ' Average Plus/Minus: ' + str(round(avg_pm_arr, 2)))