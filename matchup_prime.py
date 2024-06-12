#NBA-api imports
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playergamelog, commonteamroster, commonplayerinfo
from nba_api.stats.library.parameters import SeasonAll
import pandas as pd
import math
#ML imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error

#prime player and team dict
player_dict = players.get_players()
teams_dict = teams.get_teams()

prime_player_id = 0
prime_opp_team_id = 0

###CHANGE PLAYER, TEAM, SEASON(should ideally remain most recent season) HERE
###########################################################################
player1 = [player for player in player_dict if player['full_name'] == 'Klay Thompson'][0]
prime_player_id = player1['id']

team1_id = 0
for team in teams.get_teams():
    if team['full_name'] == 'Houston Rockets':
        prime_opp_team_id = team['id']

season = '2023-24'

###CHANGE PLAYER AND TEAM ABOVE
#############################################################################    

###HELPERS
#############################################################################
def get_matchup(player_id, opposing_team_id):
    
    #get player position
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_info_df = player_info.get_data_frames()[0]
    player_position = player_info_df.loc[0, 'POSITION']

    #get opposite team roster
    team_roster = commonteamroster.CommonTeamRoster(team_id=opposing_team_id)
    team_roster_df = team_roster.get_data_frames()[0]

    #filter all players of the same position
    same_position_players = team_roster_df[team_roster_df['POSITION']
                                        == player_position[0]]
    #return as iterable with player ids
    return same_position_players['PLAYER_ID'].tolist()


#TEST MATCHUP PRINTER
#print(get_matchup(201939, 1610612739))

#gets player logs for all past seasons
def get_player_game_logs_all_seasons(player_id):
    game_logs = playergamelog.PlayerGameLog(player_id=player_id, season=SeasonAll.all)
    return pd.DataFrame(game_logs.get_normalized_dict()['PlayerGameLog'])

#find games player1 and player2 played against each other
def find_common_games(player1_logs, player2_logs):
    common_games = pd.merge(player1_logs, player2_logs, on="Game_ID", suffixes=('_p1', '_p2'))
    return common_games

pts = []
#Evaluates player performance in common games and averages player points per matchup
def evaluate_performance_statistics(common_games):
    print("Evaluating performance metrics:")
    metrics = ['PTS_p1', 'PTS_p2', 'FG_PCT_p1', 'FG_PCT_p2', 'REB_p1', 'REB_p2', 'AST_p1', 'AST_p2', 'STL_p1', 'STL_p2']
    for metric in metrics:
        p1_avg = common_games[metric].mean()
        if metric == 'PTS_p1' and not math.isnan(p1_avg):
            pts.append(p1_avg)
        print(f"Average {metric}: {p1_avg:.2f}")

#analyzes two players performance when playing against each other
def head_to_head_analysis(player1_id, player2_id):
    print(f"Evaluating performances for Player IDs {player1_id} and {player2_id}")

    player1_logs = get_player_game_logs_all_seasons(player1_id)
    player2_logs = get_player_game_logs_all_seasons(player2_id)
    
   
    common_games = find_common_games(player1_logs, player2_logs)
    
 
    evaluate_performance_statistics(common_games)



# Example ids
#player1_id = 201939  #Stephen Curry
#player2_id = 202681  #Kyrie Irving


################################################################################


#PRINT HEAD TO HEAD DATA
for player in get_matchup(prime_player_id, prime_opp_team_id):
    print(head_to_head_analysis(prime_player_id, player))



#PREDICTION MODEL AND HELPERS
################################################################################
    
#retrieve player games for specific season (should be the latest for next game prediction purposes)
def get_player_game_logs_by_year(player_id, season='2023-24'):
    player_logs = playergamelog.PlayerGameLog(player_id=player_id, season=season).get_data_frames()[0]
    return player_logs


def preprocess_data(player_logs):
    player_logs['GAME_DATE'] = pd.to_datetime(player_logs['GAME_DATE'])
    player_logs = player_logs.sort_values(by='GAME_DATE')

    #Create lag features
    for lag in range(1, 8):
        player_logs[f'PTS_lag_{lag}'] = player_logs['PTS'].shift(lag)
        player_logs[f'REB_lag_{lag}'] = player_logs['REB'].shift(lag)
        player_logs[f'AST_lag_{lag}'] = player_logs['AST'].shift(lag)
    
    #Drop NaN rows from lagging manipulation
    player_logs = player_logs.dropna()
    
    #adds column which describes if game was at home or away for opp and player
    player_logs['HOME'] = player_logs['MATCHUP'].apply(lambda x: 1 if 'vs.' in x else 0)
    player_logs['OPPONENT'] = player_logs['MATCHUP'].apply(lambda x: x.split()[-1])
    
    return player_logs


#creates pipeline to preprocess data and 
def create_pipeline():

    numerical_features = [f'PTS_lag_{i}' for i in range(1, 8)] + [f'REB_lag_{i}' for i in range(1, 8)] + [f'AST_lag_{i}' for i in range(1, 8)]
    categorical_features = ['HOME', 'OPPONENT']
    
    #fills empty spots with mean and reduces unit variance
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])
    
    #fills empty categorical spots
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    #applies transformers to columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    #define model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    return model

#train model to predict points
def train_model(player_logs, target='PTS'):
    #pull features that are not game id, game date, points, or matchup
    features = [col for col in player_logs.columns if col not in ['GAME_ID', 'GAME_DATE', target, 'MATCHUP']]
    X = player_logs[features]
    y = player_logs[target]
    
    #separate data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    #instantiate model and train
    model = create_pipeline()
    model.fit(X_train, y_train)

    y_predicted = model.predict(X_test)
    mse = mean_squared_error(y_test, y_predicted)
    print(f"MSE:{mse}")
    
    return model

#predict performance
def predict_performance(model, upcoming_game_data):
    # Predict the performance for the upcoming game
    prediction = model.predict(upcoming_game_data)
    return prediction

###############################################################################



#MAIN
#retrieve most recent data for season and train model
player_logs = get_player_game_logs_by_year(prime_player_id, season)
player_logs_processed = preprocess_data(player_logs) 
model = train_model(player_logs_processed, target='PTS')

#drop irrelevant colums and predict on rest
#average out matchup points and predicted points
upcoming_game_data = player_logs_processed.iloc[-1:].drop(columns=['Game_ID', 'GAME_DATE', 'PTS', 'MATCHUP'])
predicted_points = predict_performance(model, upcoming_game_data)
print(f'Predicted Points: {(predicted_points[0] + sum(pts)/len(pts))/2}')
print(prime_player_id)

