from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import alltimeleadersgrids
import pandas as pd
import numpy as np


#gets the player ids with the most assists from the endpoint and returnts the players from the player dict
all_time_points = alltimeleadersgrids.AllTimeLeadersGrids().ast_leaders.get_data_frame()
player_dict = players.get_players()
teams_dict = teams.get_teams()

all_time_ast = all_time_points.to_dict()['PLAYER_ID'].values()
ast_final_list = [player['full_name'] for player in player_dict if player['id'] in all_time_ast]

print(all_time_ast)
print('\n\n')
print(ast_final_list)


