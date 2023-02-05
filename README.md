*Created by Aniq Premji*

## Background

This app predicts the top 10 most likely players to win the MVP award for the current NBA season. Individual player data from the last 40 years is scraped from the BasketballReference website in JSON format, cleaned, and stored in a MongoDB database. Next, when the user wishes to predict the MVP ladder for this season, a machine learning model is run on the data to predict the percentage of MVP shares that a player will win - the higher the number of shares, the higher on the MVP ladder they are. The players with the top 10 highest predicted shares are displayed on a Streamlit app, and the data may be refreshed on the app's home page.

https://user-images.githubusercontent.com/89875233/212566852-5272b5cd-e19c-4d78-95cb-291d608d05d1.mp4

## Motivation For Project

It is generally understood that a player's individual stats play an important role in their perception as the most valuable player of the season. In many past seasons, the MVP has been the most statistically-dominant player. However, it is also understood that a team's wins are an important consideration as well. If a player is performing well individually, but their team isn't winning games, their efforts might not be considered as valuable. As such, I wanted to see if these stats would be good predictors for the number of shares that a player received throughout a season.

Additionally, I wanted to be able to track this without having to run a manual refresh of the webscraping, data processing and machine learning processes. Since the raw data is stored in JSON files, I stored this information through a data pipeline that extracts, transforms and loads the data into a MongoDB database, that is eventually used to input data into the model.

## Data Exploration

To get an idea of feature importance, I created a correlation matrix for all the features and observed which had the strongest effect on MVP share.

<img width="325" alt="image" src="https://user-images.githubusercontent.com/89875233/216799377-4a6211dc-935b-4bfb-9840-fd95e4a6473e.png">

The most features with the strongest correlation with MVP shares seem to be free throws, points, two-pointers made, field goals attempted and rebounds. These make sense since aggressive players that tend to score and draw fouls, but also are able to rebound the ball are considered very valuable players (ex. Shaquille O'Neal, Hakeem Olajuwon, James Harden).

## Error Metric

Typical error metrics, such as MAE, R^2 and RMSE in this case would not be as effective, since the vast majority of players receive 0 MVP votes, and we don't want to give the model a high score for predicting this. I defined a custom error metric that scores the model based on how well it predicts the top 10 candidates for MVP, as these are the individuals that we want to prioritize while ranking. 

This metric compares a model's predictions to the actual top 10 MVP rankings from a specific year. If the prediction correctly selects a player who was actually in the top 10 candidates that year, it gets a 100% score for that player. If it does not correctly capture a player who was in the top 10, the score for that player gets worse and worse depending on how far out of the top 10 they were predicted to be. Ten scores are captured (one for each player), and the final metric is the average of these scores (called mean average precision).

## Model Selection

There were 3 candidates to be used for the model:

- Multiple Linear Regression
- Random Forest
- XGBoost

Each model was trained through a backtesting process; that is, testing on one year of data after training on all the prior years of data, then including that year of testing in the next iteration of training data. As such, the training window is constantly expaning to predict the MVP for the next season. This prevents overfitting by ensuring that future information about MVPs is not used in predicting MVPs from the past. 

![image](https://user-images.githubusercontent.com/89875233/210304761-d23d7b8a-6b76-4b9a-827f-b003e63814be.png)

Through many iterations of manual feature selection by intuition, and hyperparameter tuning through GridSearchCV with a Time Series Split, the model with the best mean average precision was XGBoost with the following parameters:

```{n_estimators=16, max_depth=5, learning_rate = 0.2745, subsample=1, colsample_bytree=1}```

This model was then used in predicting the most likely MVP candidates for the 2022-2023 season.

It will be interesting to follow the model's predictions as the 2022-23 NBA season progresses, and we gain more data about who is the league's most valuable player.
