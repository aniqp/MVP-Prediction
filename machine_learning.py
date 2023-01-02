import pandas as pd
from sklearn.preprocessing import StandardScaler

def get_top_10():

       stats = pd.read_csv("player_mvp_stats.csv")
       stats_2023 = pd.read_csv("player_mvp_stats_2023.csv")
       stats = stats.fillna(0)
       stats_2023 = stats_2023.fillna(0)
       stats['Age'] = stats['Age'].astype(int)
       # Numeric columns are the ones we want to use as predictors. Don't use pts won/pts max/share - these are very related with what we are trying to predict (overfitting)
       predictors = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
              '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
              'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'W/L%', 'GB', 'PS/G',
              'PA/G', 'SRS']

       predictors.append('Year')
       train = stats[stats["Year"] < 2023]

       # Don't test on data that is before data you're training on (this would cause overfitting)
       test = stats_2023

       from sklearn.linear_model import Ridge

       # Alpha is how much the linear regression coefficient is shrunk to prevent overfitting
       reg = Ridge(alpha = 0.1)
       reg.fit(train[predictors], train["Share"])
       predictions = reg.predict(test[predictors])
       predictions = pd.DataFrame(predictions, columns = ['predictions'], index = test.index)
       combination = pd.concat([test[["Player", "Share"]], predictions], axis = 1)
       return combination.sort_values("predictions", ascending = False).head(10)['Player'].values
# def find_average_precision_new():
#     # Take the top 5 MVP winners
#     actual = actual_mvp
#     predicted = combination.sort_values("predictions", ascending = False)
#     ps = []
#     found = 0
#     seen = 1
#     # if predicted player is in top 10, we get 100%, but if not, then penalize based on how far off
#     # biased towards top of the ranking (rank in top 10 a lot more important than rank outside)
#     for index, row in predicted.iterrows():        
#         if row["Player"] in actual['Player'].values:
#             found += 1
#             print(f'found: {found}, seen: {seen}')            
#             ps.append(found/seen)
#         seen += 1
#     return ps, (sum(ps) / len(ps))

# predictions = ['Luka Dončić', 'Giannis Antetokounmpo', 'Joel Embiid', 'Nikola Jokić', 'Anthony Davis', 'Kevin Durant', 'Shai Gilgeous-Alexander', 'Stephen Curry',
# 'Jayson Tatum', 'Ja Morant']

# print(predictions)