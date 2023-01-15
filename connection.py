from pymongo import MongoClient
from pymongo import UpdateOne
from bson.objectid import ObjectId
import pandas as pd
from config import MONGODB_URI

MONGODB_URI = MONGODB_URI

client = MongoClient(MONGODB_URI)

db = client.MVP_Data

mvp_collection = db.MVP

players_2023_stats = pd.read_csv("player_mvp_stats_2023.csv")
players_2023_stats[~players_2023_stats['Player'].isna()]

def update_player_data():

    player_list = []

    for i in range(len(players_2023_stats)):
        player = players_2023_stats['Player'].iloc[i]
        player_list.append({player : {}})
        for column in players_2023_stats.columns.delete(0):
            player_list[i][player][column] = players_2023_stats[column].iloc[i]

    requests = []
    for player in player_list:
        for player_name, stats in player.items():
            requests.append(UpdateOne( {'Player': player_name },  {'$set': {
            "Pos":stats['Pos'],
            "Age":float(stats['Age']),
            "Tm":stats['Tm'],
            "G":float(stats['G']),
            "GS":float(stats['GS']),
            "MP":float(stats['MP']),
            "FG":float(stats['FG']),
            "FGA":float(stats['FGA']),
            "FG%":float(stats['FG%']),
            "3P":float(stats['3P']),
            "3PA":float(stats['3PA']),
            "3P%":float(stats['3P%']),
            "2P":float(stats['2P']),
            "2PA":float(stats['2PA']),
            "2P%":float(stats['2P%']),
            "eFG%":float(stats['eFG%']),
            "FT":float(stats['FT%']),
            "FTA":float(stats['FTA']),
            "FT%":float(stats['FT%']),
            "ORB":float(stats['3P%']),
            "DRB":float(stats['DRB']),
            "TRB":float(stats['TRB']),
            "AST":float(stats['AST']),
            "STL":float(stats['STL']),
            "BLK":float(stats['BLK']),
            "TOV":float(stats['TOV']),
            "PF":float(stats['PF']),
            "PTS":float(stats['PTS']),
            "Year":int(stats['Year']),
            "Team":stats['Team'],
            "W":int(stats['W']),
            "L":int(stats['L']),
            "W/L%":float(stats['W/L%']),
            "GB":float(stats['GB']),
            "PS/G":float(stats['PS/G']),
            "PA/G":float(stats['PA/G']),
            "SRS":float(stats['SRS'])
            }}))

    results = mvp_collection.bulk_write(requests)
    return results

def get_player_data():
    documents_to_find = {'Year': {'$eq' : 2023}}
    result = mvp_collection.find(documents_to_find)
    return result

cursor = get_player_data()

list = []
for document in cursor:
    list.append(document)

new_test_data = pd.DataFrame(list)