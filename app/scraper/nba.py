"""Pull down NBA data"""
import requests
from flask_pymongo import MongoClient

CLIENT = MongoClient()
DB = CLIENT.fantasy

print("runnning")

def create_player_db():
    """Makes a new database with everyones name"""
    players = DB.players
    people = ["Bryan Hee", "Jake Doering", "Matt Sweeney", "Kyle Mayer", "Brian St\
    ern", "Alex Gunning", "Tim Erdmann", "Brian Clifford", "Sam Levitt", "Armen Vop\
    ain", "Aman Kiflezgi", "Joe Kovach"]
    for i, person in enumerate(people):
        i += 1
        dude = {"name": person}
        print(dude)
        _ = players.insert(dude).inserted_id

def create_nba_db():
    """Makes a new database for the nba"""
    players = DB.players
    nba = DB.nba

    teams = ["Celtics", "Cavaliers", "Raptors", "Wizards", "Hawks", "Bucks", \
    "Pacers", "Bulls", "Heat", "Pistons", "Hornets", "Knicks"]

    cursor = players.find()
    for team, document in zip(teams, cursor):
        data = {"_id": document['_id'], "team": team}
        _ = nba.insert(data)


#Get the json data for the progam
def get_standings():
    """Get the json data for the progam"""
    res = requests.get("https://erikberg.com/nba/standings.json")
    return res.json()['standing']

def update_standings():
    """Update the NBA standings in the database"""
    nba = DB.nba
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

update_standings()
