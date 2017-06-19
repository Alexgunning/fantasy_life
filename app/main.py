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
        team['user_name'] = players.find_one({"_id": team["associated_player_id"]})["name"]
        output.append(team)
    return render_template('layout.html', teams=output, table_name="NBA")

@app.route('/mlb', methods=['GET'])
def get_mlb_data():
    """Get mlb data"""
    mlb = mongo.db.mlb
    players = mongo.db.players
    teams = []
    for team in mlb.find().sort("win_precentage", -1):
        team['user_name'] = players.find_one({"_id": team["associated_player_id"]})["name"]
        teams.append(team)
    return render_template('layout.html', teams=teams, table_name="MLB")

@app.route('/pga', methods=['GET'])
def get_pga_data():
    """Get pga data"""
    pga = mongo.db.pga
    players = mongo.db.players
    table_data = []
    for golfer in pga.find().sort("rank", 1):
        #Get player name asscoiated with golfer
        golfer['user_name'] = players.find_one({"_id": golfer["associated_player_id"]})["name"]
        table_data.append(golfer)

    return render_template('ranking_layout.html', table_data=table_data, table_name="PGA")

@app.route('/atp', methods=['GET'])
def get_atp_data():
    """Get atp data"""
    atp = mongo.db.atp
    players = mongo.db.players
    table_data = []
    for tennis_player in atp.find().sort("rank", 1):
        #Get player name asscoiated with golfer
        tennis_player['user_name'] = players.find_one({"_id": tennis_player["associated_player_id"]})["name"]
        table_data.append(tennis_player)

    return render_template('ranking_layout.html', table_data=table_data, table_name="ATP")

@app.route('/nascar', methods=['GET'])
def get_nascar_data():
    """Get nascar data"""
    nascar = mongo.db.nascar
    players = mongo.db.players
    table_data = []
    for driver in nascar.find().sort("rank", 1):
        #Get player name asscoiated with golfer
        driver['user_name'] = players.find_one({"_id": driver["associated_player_id"]})["name"]
        table_data.append(driver)

    return render_template('ranking_layout.html', table_data=table_data, table_name="NASCAR")

@app.route('/stocks', methods=['GET'])
def get_stock_data():
    """Get  data"""
    stocks = mongo.db.stocks
    players = mongo.db.players
    table_data = []
    for stock in stocks.find().sort("delta", -1):
        #Get player name asscoiated with the stock
        stock['user_name'] = players.find_one({"_id": stock["associated_player_id"]})["name"]
        table_data.append(stock)

    return render_template('stocks_template.html', stocks=table_data, table_name="Stocks")

@app.route('/music', methods=['GET'])
def get_music_data():
    """Get  data"""
    musicians = mongo.db.musicians
    players = mongo.db.players
    table_data = []
    for artist in musicians.find().sort("score", -1):
        #Get player name asscoiated with the artist
        artist['user_name'] = players.find_one({"_id": artist["associated_player_id"]})["name"]
        table_data.append(artist)

    return render_template('music_template.html', artists=table_data, table_name="Music")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
