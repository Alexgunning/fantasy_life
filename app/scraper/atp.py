"""Pull down NBA data"""
import requests
from flask_pymongo import MongoClient
from lxml import html

client = MongoClient()
db = client.fantasy

print("runnning atp")

#TODO Tie ids to a new object id and associate it with a user id

def create_atp_db():
    """Makes a new database for the nba"""
    player_view_names = ["Andy Murray", "Rafael Nadal", "Stan Wawrinka", "Novak Djokovic",\
    "Dominic Thiem", "Grigor Dimitrov", "David Goffin", "Tomas Berdych",\
    "Gael Monfils", "Jack Sock", "Nick Kyrgios", "Albert Ramos-Vinolas"]

    player_web_names = [player.lower().replace(' ', '-') for player in player_view_names]

    players = db.players
    atp = db.atp
    atp.drop()
    user = players.find()
    for player_web_name, player_view_name, user in zip(player_web_names, player_view_names, user):
        data = {"associated_player_id": user['_id'], "player_web_name": player_web_name, "name" : player_view_name}
        _ = atp.insert(data)

def get_player_ranking():
    """get the json data for the progam"""
    res = requests.get("http://www.espn.com/tennis/rankings")
    tree = html.fromstring(res.content)

    atp = db.atp

    tennis_players = [str(tennis_player["player_web_name"]) for tennis_player in atp.find()]

    tree = html.fromstring(res.content)
    table = tree.find_class("tablehead")
    player_links = [player_link for player_link in table[0].iterlinks() if player_link[1] == 'href']

    counter = 0
    for link in player_links:
        player_link_name = link[2].split('/')[-1]
        if player_link_name in tennis_players:
            rank = int(link[0].getparent().getprevious().text_content())
            atp.update_one({
                'player_web_name': player_link_name
            }, {
                '$set': {
                    'rank': rank
                }
            })
            counter += 1
            if counter == len(tennis_players):
                break

create_atp_db()
get_player_ranking()

