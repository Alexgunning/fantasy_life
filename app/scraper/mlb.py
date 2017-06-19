"""Pull down MLB data"""
import requests
from flask_pymongo import MongoClient

CLIENT = MongoClient()
DB = CLIENT.fantasy

print("runnning")

def create_mlb_db():
    """Makes a new database for the nba"""
    players = DB.players
    mlb = DB.mlb

    teams = ['Twins', 'Indians', 'Tigers', 'Royals', 'White Sox', 'Angels', \
    'Red Sox', 'Rays', 'Orioles', 'Blue Jays', 'Astros', 'Yankees']

    users = players.find()
    for team, user in zip(teams, users):
        data = {"associated_player_id": user['_id'], "team": team}
        _ = mlb.insert(data)


#Get the json data for the progam
def get_standings():
    """Get the json data for the progam"""
    res = requests.get("https://erikberg.com/mlb/standings.json")
    return res.json()['standing']

def update_standings():
    """Update the NBA standings in the database"""
    mlb = DB.mlb
    teams = [team["team"] for team in mlb.find()]
    standings = get_standings()
    for team in standings:
        if team['last_name'] in teams:
            mlb.update_one({
                'team': team['last_name']
                }, {
                    '$set': {
                        'won': team['won'],
                        'lost': team['lost'],
                        'win_precentage' : team['win_percentage']
                    }
                })

create_mlb_db()
update_standings()
