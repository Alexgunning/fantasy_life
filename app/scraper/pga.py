"""Pull down PGA data"""
import re
import requests
from flask_pymongo import MongoClient
from lxml import html

client = MongoClient()
db = client.fantasy

print("runnning pga")

#TODO Tie ids to a new object id and associate it with a user id

def create_pga_db():
    """Makes a new database for the nba"""
    golfers = ["Dustin Johnson", "Rory McIlroy", "Jason Day", "Sergio Garcia",\
     "Jordan Spieth", "Rickie Fowler", "Justin Rose", "Adam Scott",\
     "Paul Casey", "Matt Kuchar", "Kevin Kisner", "Phil Mickelson"]

    players = db.players
    pga = db.pga
    cursor = players.find()
    for golfer, document in zip(golfers, cursor):
        data = {"_id": document['_id'], "golfer": golfer}
        _ = pga.insert(data)


#Get the json data for the progam
def get_player_ranking():
    """Get the json data for the progam"""
    pga = db.pga
    res = requests.get("http://www.pgatour.com/stats/stat.186.html")
    tree = html.fromstring(res.content)

    web_ids = [str(golfers["web_id"]) for golfers in pga.find()]

    #Get the first child of the talbe row element aand string the whitespace
    for web_id in web_ids:
        web_id_path = "playerStatsRow%s"%web_id
        ranking = tree.get_element_by_id(web_id_path)[0].text_content().strip()
        ranking = int(ranking)
        pga.update_one({
            'web_id': web_id
        }, {
            '$set': {
                'ranking': ranking
            }
        })

def scrape_player_ids():
    """Get the pga tour webpage id's"""
    res = requests.get("http://www.pgatour.com/stats/stat.186.html")
    tree = html.fromstring(res.content)
    pga = db.pga
    golfers = [str(golfers["golfer"]) for golfers in pga.find()]
    table = tree.find_class("details-table-wrap")

    #TODO CLEAN UP wasted loop cycles
    #Go through each link in table
    for link in table:
        counter = 0
        for j in link.iterlinks():
            #Get the text content and sanitize it
            name = str((j[0].text_content())).strip().replace('\xa0', ' ')
            if name in golfers:
                href = str(j[2])
                digits = re.findall(r"\d+", href)[0]
                pga.update_one({
                    'golfer': name
                }, {
                    '$set': {
                        'web_id': digits
                    }
                })
                #Break from loop if all golfers updated
                counter += 1
                if counter == len(golfers):
                    break

scrape_player_ids()
get_player_ranking()

print("done")
