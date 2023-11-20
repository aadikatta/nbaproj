from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import alltimeleadersgrids
import pandas as pd
import numpy as np

all_time_points = alltimeleadersgrids.AllTimeLeadersGrids().ast_leaders.get_data_frame()
player_dict = players.get_players()
teams_dict = teams.get_teams()

all_time_ast = all_time_points.to_dict()


#player_names = [player['id'] for player in player_dict if player['id'] in all_time_points['data']]
#print(all_time_ast[0][0] for player in all_time_ast)


ast_player_ids = all_time_ast['PLAYER_ID'].values()

ast_player_list = [player for player in ast_player_ids]

ast_final_list = [player['full_name'] for player in player_dict if player['id'] in ast_player_list]

print(ast_player_list)
print('\n\n')
print(ast_final_list)


