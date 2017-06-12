"""Server html for the main fantasy page"""
from flask import Flask, render_template, jsonify
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
    print("\nIn NBAn\n")
    nba = mongo.db.nba
    players = mongo.db.players
    output = []
    for team in nba.find():
        name = players.find_one({"_id": team["_id"]})["name"]
        output.append({'name': name, 'team' : team['team'], 'won' : team['won'], 'lost' :\
        team['lost'], 'win_precentage' : team['win_precentage']})
    return render_template('layout.html', teams=output)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
