"""Pull down NFL data"""
import requests
from flask_pymongo import MongoClient
from lxml import html

client = MongoClient()
db = client.fantasy

print("runnning nfl")

#TODO Tie ids to a new object id and associate it with a user id

def create_nfl_db():
    """Makes a new database for the nba"""

    team_view_names = ['Buffalo Bills', 'New York Jets', 'Pittsburgh Steelers', 'Baltimore Ravens',\
    'Cincinnati Bengals', 'Cleveland Browns', 'Tennessee Titans', 'Indianapolis Colts',\
    'Jacksonville Jaguars', 'Los Angeles Chargers', 'Philadelphia Eagles', 'San Francisco 49ers']

    team_web_names = [team.lower().replace(' ', '-') for team in team_view_names]

    players = db.players
    nfl = db.nfl
    nfl.drop()
    users = players.find()
    for team_web_name, team_view_name, user in zip(team_web_names, team_view_names, users):
        data = {"associated_player_id": user['_id'], "team_web_name": team_web_name, "name" :\
        team_view_name}
        _ = nfl.insert(data)

def get_player_ranking():
    """get the json data for the progam"""
    res = requests.get("http://www.cbssports.com/nfl/standings")
    tree = html.fromstring(res.content)

    nfl = db.nfl

    teams = [str(team["team_web_name"]) for team in nfl.find()]

    tree = html.fromstring(res.content)
    table = tree.find_class("data stacked")

    #flatten out division
    #CBS divides each division into a table so put all teams back into a list
    team_links = []
    for division in table:
        division_links = [player_link for player_link in division.iterlinks() if player_link[1] == 'href']
        team_links.extend(division_links)

    counter = 0
    for link in team_links:
        team_link_name = link[2].split('/')[-1]
        if team_link_name in teams:

            wins = int(link[0].getparent().getnext().text_content())
            losses = int(link[0].getparent().getnext().getnext().text_content())
            ties = int(link[0].getparent().getnext().getnext().getnext().text_content())

            win_pct = wins/(wins + losses)

            nfl.update_one({
                'team_web_name': team_link_name
            }, {
                '$set': {
                    'won': wins,
                    'lost': losses,
                    'tie': ties,
                    'win_precentage' : win_pct
                }
            })
            counter += 1
            if counter == len(teams):
                break

create_nfl_db()
get_player_ranking()

