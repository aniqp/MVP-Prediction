import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(chrome_options=options)
import time

def get_player_stats():
    player_stats_url = "https://www.basketball-reference.com/leagues/NBA_2023_per_game.html"
    driver.get(player_stats_url)
    driver.execute_script("window.scrollTo(1,10000)")
    time.sleep(2)

    html=driver.page_source

    with open("player/2023.html", "w+", encoding = "utf-8") as f:
        f.write(html)

    with open("player/2023.html", encoding = "utf-8") as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_='thead').decompose()
    player_table = soup.find_all(id = "per_game_stats")
    player_2023 = pd.read_html(str(player_table))[0]
    player_2023["Year"] = 2023

    print(player_2023)

    player_2023.to_csv("player_2023.csv")

def get_team_stats():
    team_stats_url = "https://www.basketball-reference.com/leagues/NBA_2023_standings.html"
    data = requests.get(team_stats_url)
    with open("team/2023.html", "w+", encoding = "utf-8") as f:
        f.write(data.text)

    with open("team/2023.html", encoding = "utf-8") as f:
        page = f.read()
    dfs = []
    soup = BeautifulSoup(page, 'html.parser')
    soup.find('tr', class_="thead").decompose()
    e_table = soup.find_all(id="divs_standings_E")[0]
    e_df = pd.read_html(str(e_table))[0]
    e_df["Year"] = 2023
    e_df["Team"] = e_df["Eastern Conference"]
    del e_df["Eastern Conference"]
    dfs.append(e_df)
    
    w_table = soup.find_all(id="divs_standings_W")[0]
    w_df = pd.read_html(str(w_table))[0]
    w_df["Year"] = 2023
    w_df["Team"] = w_df["Western Conference"]
    del w_df["Western Conference"]
    dfs.append(w_df)

    teams_2023 = pd.concat(dfs)

    def get_ind_not_alpha(x):
        count = 0
        for char in x:
            print(char)
            count = count +1
            if (char.isalnum() == False) & (char != ' '):
                return(count - 1)

    teams_2023['Team'] = teams_2023['Team'].apply(lambda x: x[:get_ind_not_alpha(x)])

    print(teams_2023)

    teams_2023.to_csv("teams_2023.csv")

def clean_data():
    players = pd.read_csv("player_2023.csv")
    del players["Unnamed: 0"]
    del players["Rk"]
    players['Player'] = players["Player"].str.replace("*", "", regex = False)
    def single_row(df):
        # if there is only one row, don't do processing
        if df.shape[0] == 1:
            return df
        else:
            row = df[df['Tm'] == "TOT"]
            # if this person played for multiple teams, replace them with the last team they played with
            row["Tm"] = df.iloc[-1,:]["Tm"]

        # Making a group for each player/year combination and for this group, only keep one unique row (with the last team they played for)
    players = players.groupby(["Player", "Year"]).apply(single_row)
    players.index = players.index.droplevel()
    players.index = players.index.droplevel()

    players[['Pts Won', 'Pts Max', 'Share']] = 0

    teams = pd.read_csv("teams_2023.csv")
    teams = teams[~teams["W"].str.contains("Division")]
    teams["Team"] = teams["Team"].str.replace("*", "", regex = False)
    nicknames = {}
    with open("nicknames.csv") as f:
        lines = f.readlines()
        for line in lines[1:]:
            # split this by comma 
            abbrev,name = line.replace("\n", "").split(",")
            nicknames[abbrev] = name
    players["Team"] = players["Tm"].map(nicknames)
    stats = players.merge(teams, how = "outer", on = ["Team", "Year"])
    del stats["Unnamed: 0"]
    stats = stats.apply(pd.to_numeric, errors = "ignore")
    stats["GB"] = stats['GB'].str.replace("???", "0")
    stats['GB'] = pd.to_numeric(stats["GB"])
    stats.to_csv("player_mvp_stats_2023.csv", index = False)

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

print(get_top_10())