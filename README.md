We do not condone or take part in gambling.


Uses player matchups and previous performance to predict a player's points in a coming game against a specified opposing team. 

**Main functionality will be found in matchup_prime.py.


Isolate player performance for each possible matchup on the other team by position, and average our player's performance for all matchups.

Create lagged features to understand how all other factors in player log can affect performance. OneHotEncoder used for categoricl data. Holes in data filled by Imputer and added by column transformer.

Game ID, Game Date, Points, and Matchup dropped from the learning set. Then, we split into train and test, and fit our model. MSE is calculated for points prediction based on the test set.



In the coming weeks we want to:
- Add functionality for assists, rebounds, and first-half points
- Add a WNBA option
- Weight more recent games more heavily, especially by year
- Automatically populate predictions by scraping PrizePicks website

