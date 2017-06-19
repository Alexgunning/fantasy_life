"""Pull down NBA data"""
import requests
from flask_pymongo import MongoClient

client = MongoClient()
db = client.fantasy

print("runnning")

def create_player_db():
    """Makes a new database with everyones name"""
    players = db.players
    players.drop()

    people = ["Bryan Hee", "Jake Doering", "Matt Sweeney", "Kyle Mayer", "Brian Stern",\
    "Alex Gunning", "Tim Erdmann", "Brian Clifford", "Sam Levitt", "Armen Vopain",\
    "Aman Kiflezgi", "Joe Kovach"]
    for person in people:
        _ = players.insert({"name": person})

def create_nba_db():
    """Makes a new database for the nba"""
    players = db.players
    nba = db.nba
    nba.drop()

    teams = ["Celtics", "Cavaliers", "Raptors", "Wizards", "Hawks", "Bucks", \
    "Pacers", "Bulls", "Heat", "Pistons", "Hornets", "Knicks"]

    users = players.find()
    for team, user in zip(teams, users):
        data = {"associated_player_id": user['_id'], "team": team}
        _ = nba.insert(data)

#Get the json data for the progam
def get_standings():
    """Get the json data for the progam"""
    res = requests.get("https://erikberg.com/nba/standings.json")
    return res.json()['standing']

def update_standings():
    """Update the NBA standings in the database"""
    nba = db.nba
    teams = [team["team"] for team in nba.find()]
    standings = get_standings()
    for team in standings:
        if team['last_name'] in teams:
            nba.update_one({
                'team': team['last_name']
                }, {
                    '$set': {
                        'won': team['won'],
                        'lost': team['lost'],
                        'win_precentage' : team['win_percentage']
                    }
                })

#create_player_db()
# create_nba_db()
update_standings()
