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

def player_vs_player(player1, player2):
    player1_name = player1
    player2_name = player2

    #Will return the stats of two players that played in games where the other player played in both of their careers
    #Works for players that played on the same team or against each other

    player1 = [player for player in player_dict if player['full_name'] == player1_name][0]
    player1_id = player1['id']
    player2 = [player for player in player_dict if player['full_name'] == player2_name][0]
    player2_id = player2['id']

    #change SeasonAll."previous_season" to retrieve seasons other than that one
    #eventually should be able to be changed upon input?
    player1_games = playergamelog.PlayerGameLog(player_id=player1_id, season=SeasonAll.all).get_normalized_dict()
    player1_games_dict = player1_games['PlayerGameLog']
    player1_print = [game["Game_ID"] for game in player1_games_dict]

    player2_games = playergamelog.PlayerGameLog(player_id=player2_id, season=SeasonAll.all).get_normalized_dict()
    player2_games_dict = player2_games['PlayerGameLog']
    player2_print = [game["Game_ID"] for game in player2_games_dict]
    player2_full = [game for game in player2_games_dict]

    player2vsplayer1_dict = [game_id for game_id in player2_print if game_id in player1_print]

    player1vs_dict = [game for game in player1_games_dict if game['Game_ID'] in player2vsplayer1_dict]
    player2vs_dict = [game for game in player2_games_dict if game['Game_ID'] in player2vsplayer1_dict]

    '''print(player1_games_dict)
    print('\n\n\n')'''

    #print(player2vsplayer1_dict)

    print('\n\n\n')


    #calculations + data retrieval
    print('----------------' + player1_name + '----------------')
    print([(game['PTS'], game['FG_PCT'], game['PLUS_MINUS'], game['MATCHUP'], game['GAME_DATE']) for game in player1vs_dict])

    print('\n\n')

    print('----------------' + player2_name + '----------------')
    print([(game['PTS'], game['FG_PCT'], game['PLUS_MINUS'], game['MATCHUP'], game['GAME_DATE']) for game in player2vs_dict])

    #print statements

    print('\n\n\n')
    player1_points_avg = round(np.mean([(game['PTS']) for game in player1vs_dict]), 2)              #points average calculation
    print(player1_name + ' Points Average: ' + str(player1_points_avg))                        
    avg_pm_arr = np.mean([(game['PLUS_MINUS']) for game in player1vs_dict])                         #Plus/Minus average calculation              
    print(player1_name + ' Average Plus/Minus: ' + str(round(avg_pm_arr, 2)))


    print('\n\n\n')
    player2_points_avg = round(np.mean([(game['PTS']) for game in player2vs_dict]), 2)
    print(player2_name + ' Points Average: ' + str(player2_points_avg))
    avg_pm_arr = np.mean([(game['PLUS_MINUS']) for game in player2vs_dict])
    print(player2_name + ' Average Plus/Minus: ' + str(round(avg_pm_arr, 2)))





#MAIN
player_vs_player('Stephen Curry', 'LeBron James')