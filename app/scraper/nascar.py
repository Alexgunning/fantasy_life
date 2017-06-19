"""Pull down NASCAR data"""
import requests
from flask_pymongo import MongoClient
from lxml import html

client = MongoClient()
db = client.fantasy

print("runnning nascar")

#TODO Tie ids to a new object id and associate it with a user id

def create_nascar_db():
    """Makes a new database for the nba"""

    player_web_names = ['jimmie-johnson', 'kyle-larson', 'martin-truex-jr', 'brad-keselowski',\
     'ricky-stenhouse-jr', 'ryan-newman', 'kyle-busch', 'chase-elliott', 'matt-kenseth',\
     'dale-earnhardt-jr', 'derrike-cope', 'danica-patrick']

    player_view_names = [player.title().replace('-',' ') for player in player_web_names]

    players = db.players
    nascar = db.nascar
    nascar.drop()

    user = players.find()

    for player_web_name, player_view_name, user in zip(player_web_names, player_view_names, user):
        data = {"associated_player_id": user['_id'], "player_web_name": player_web_name,\
        "name" : player_view_name}
        _ = nascar.insert(data)

def get_racer_ranking():
    """get the json data for the progam"""
    res = requests.get("http://www.espn.com/rpm/standings")
    tree = html.fromstring(res.content)

    nascar = db.nascar

    drivers = [str(racer["player_web_name"]) for racer in nascar.find()]

    tree = html.fromstring(res.content)
    table = tree.find_class("tablehead")
    player_links = [player_link for player_link in table[0].iterlinks() if player_link[1] == 'href']

    counter = 0
    for link in player_links:
        player_link_name = link[2].split('/')[-1]
        if player_link_name in drivers:
            rank = int(link[0].getparent().getprevious().text_content())
            nascar.update_one({
                'player_web_name': player_link_name
            }, {
                '$set': {
                    'rank': rank
                }
            })
            counter += 1
            if counter == len(drivers):
                break

create_nascar_db()
get_racer_ranking()

