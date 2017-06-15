#!/bin/python
"""Pull down PGA data"""
import requests
from flask_pymongo import MongoClient
from lxml import html

client = MongoClient()
db = client.fantasy

print("runnning pga")

#TODO Tie ids to a new object id and associate it with a user id

def create_pga_db():
    """Makes a new database for the nba"""
    player_view_names = ["Dustin Johnson", "Rory McIlroy", "Jason Day", "Sergio Garcia",\
     "Jordan Spieth", "Rickie Fowler", "Justin Rose", "Adam Scott",\
     "Paul Casey", "Matt Kuchar", "Kevin Kisner", "Phil Mickelson"]

    player_web_names = [player.replace(' ', '\xa0') for player in player_view_names]

    players = db.players
    pga = db.pga

    #Drop old collection if making a new one
    pga.drop()
    users = players.find()
    for player_web_name, player_view_name, users in zip(player_web_names, player_view_names, users):
        data = {"associated_player_id": users['_id'], "player_web_name": player_web_name, "name" : player_view_name}
        _ = pga.insert(data)


def get_pga_data():
    """Get the pga tour webpage id's"""
    res = requests.get("http://www.pgatour.com/stats/stat.186.html")
    tree = html.fromstring(res.content)
    pga = db.pga
    golfers = [str(golfers["player_web_name"]) for golfers in pga.find()]
    table = tree.find_class("table-styled")

    counter = 0
    for link in table[0].iterlinks():
        #Get the text content and sanitize it
        player_link_name = str(link[0].text_content())
        if player_link_name in golfers:
            rank = int(link[0].getparent().getprevious().getprevious().text_content())
            pga.update_one({
                'player_web_name': player_link_name
            }, {
                '$set': {
                    'rank': rank
                }
            })
            #Break from loop if all golfers updated
            counter += 1
            if counter == len(golfers):
                break

create_pga_db()
get_pga_data()

print("done")
