"""Server html for the main fantasy page"""
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = "fantasy"
mongo = PyMongo(app)

print("config setup\n\n")

@app.route('/')
def hello():
    """Hello World Rout"""
    return "hello world"

@app.route('/nba', methods=['GET'])
def get_nba_data():
    """Get nba data"""
    nba = mongo.db.nba
    players = mongo.db.players
    output = []
    for team in nba.find().sort("win_precentage", -1):
        team['user_name'] = players.find_one({"_id": team["_id"]})["name"]
        output.append(team)
    return render_template('layout.html', teams=output, table_name="NBA")

@app.route('/mlb', methods=['GET'])
def get_mlb_data():
    """Get mlb data"""
    mlb = mongo.db.mlb
    players = mongo.db.players
    teams = []
    for team in mlb.find().sort("win_precentage", -1):
        team['user_name'] = players.find_one({"_id": team["_id"]})["name"]
        teams.append(team)
    return render_template('layout.html', teams=teams, table_name="MLB")

@app.route('/pga', methods=['GET'])
def get_pga_data():
    """Get pga data"""
    pga = mongo.db.pga
    players = mongo.db.players
    output = []
    for golfer in pga.find().sort("ranking", 1):
        #Get player name asscoiated with golfer
        golfer['user_name'] = players.find_one({"_id": golfer["_id"]})["name"]
        output.append(golfer)

    return render_template('ranking_layout.html', golfers=output, table_name="PGA")

# get_pga_data()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
