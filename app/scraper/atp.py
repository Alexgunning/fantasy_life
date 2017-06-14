"""Pull down NBA data"""
import re
import requests
from flask_pymongo import MongoClient
from lxml import html

client = MongoClient()
db = client.fantasy

print("runnning atp")

#TODO Tie ids to a new object id and associate it with a user id

def create_atp_db():
    """Makes a new database for the nba"""
    player_names = ["Andy Murray", "Rafael Nadal", "Stan Wawrinka", "Novak Djok\
    ovic", "Dominic Thiem", "Grigor Dimitrov", "David Goffin", "Tomas Berdych",\
    "Gael Monfils", "Jack Sock", "Nick Kyrgios", "Albert Ramos-Vinolas"]

    players = db.players
    atp = db.atp
    cursor = players.find()
    for player, fantasy_player_name in zip(player_names, cursor):
        data = {"associtaed_player_id": fantasy_player_name['_id'], "tennis_player": player}
        _ = atp.insert(data)


#Get the f data for the progam

def get_player_ranking():
    """Get the json data for the progam"""
    res = requests.get("http://www.espn.com/tennis/rankings")
    tree = html.fromstring(res.content)

    atp = db.atp

    tennis_players = [str(tennis_player["tennis_player"]) for tennis_player in atp.find()]

    #Example
    #andy-murray
    player_web_names = [player.lower().replace(' ', '-') for player in tennis_players]
    print(player_web_names)

    tree = html.fromstring(res.content)
    table = tree.find_class("tablehead")
    player_links = [player_link for player_link in table[0].iterlinks() if player_link[1] == 'href']
    for link in player_links:
        print(link)

get_player_ranking()

