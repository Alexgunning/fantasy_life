"""Create all of the database relevant informatoin"""
from flask_pymongo import MongoClient

client = MongoClient()
db = client.fantasy

def convert_name_to_view_name(self, name):
    return name.title().replace('-', ' ')

def create_player_db():
    """Makes a new database with everyones name"""
    players = db.players
    players.drop()

    people = ["Bryan Hee", "Jake Doering", "Matt Sweeney", "Kyle Mayer", "Brian Stern",\
    "Alex Gunning", "Tim Erdmann", "Brian Clifford", "Sam Levitt", "Armen Vopain",\
    "Aman Kiflezgi", "Joe Kovach"]
    for person in people:
        _ = players.insert({"name": person})

def create_category_db(collection_name, items, has_name_view=False):
    """Makes a new database for the nba"""
    players = db.players
    collection = db[collection_name]
    collection.drop()

    users = players.find()

    for item, user in zip(items, users):
        data = {"associated_player_id": user['_id'], "item_view_name": item}
        _ = collection.insert(data)

class nba_db():
    """Class for creating nba database"""

    db_name = "nba"
    items = ["Celtics", "Cavaliers", "Raptors", "Wizards", "Hawks", "Bucks",\
    "Pacers", "Bulls", "Heat", "Pistons", "Hornets", "Knicks"]
    def convert_name_web_to_view(self, name):
        return name

class atp_db():
    """Class for creating atp database"""

    db_name = "atp"
    items = ['andy-murray', 'rafael-nadal', 'stan-wawrinka', 'novak-djokovic', 'dominic-thiem',\
    'grigor-dimitrov', 'david-goffin', 'tomas-berdych', 'gael-monfils', 'jack-sock',\
    'nick-kyrgios', 'albert-ramos-vinolas']
    def convert_name_web_to_view(self, name):
        return name.title().replace('-', ' ')

class mlb_db():
    """Makes a new database for the nba"""

    db_name = "mlb"
    items = ['Twins', 'Indians', 'Tigers', 'Royals', 'White Sox', 'Angels', \
    'Red Sox', 'Rays', 'Orioles', 'Blue Jays', 'Astros', 'Yankees']
    def convert_name_web_to_view(self, name):
        return name

class music_db():
    """Makes a new database for music"""

    db_name = "music"
    items = ['Bruno Mars', 'Ed Sheeran', 'Kendrick Lamar', 'Future', 'Lil Uzi Vert',\
     'James Arthur', 'Julia Michaels', 'Imagine Dragons', 'Sam Hunt', 'Taylor Swift',\
     'Katy Perry', 'Justin Bieber']
    def convert_name_web_to_view(self, name):
        return name

class nascar_db():
    """Makes a new database for nascar"""

    db_name = "nascar"
    items = ['jimmie-johnson', 'kyle-larson', 'martin-truex-jr', 'brad-keselowski',\
     'ricky-stenhouse-jr', 'ryan-newman', 'kyle-busch', 'chase-elliott', 'matt-kenseth',\
     'dale-earnhardt-jr', 'derrike-cope', 'danica-patrick']
    def convert_name_web_to_view(self, name):
        return name.title().replace('-', ' ')

class nfl_db():
    """Makes a new database for nfl"""

    db_name = "nfl"
    items = ['buffalo-bills', 'new-york-jets', 'pittsburgh-steelers', 'baltimore-ravens',\
    'cincinnati-bengals', 'cleveland-browns', 'tennessee-titans', 'indianapolis-colts',\
    'jacksonville-jaguars', 'los-angeles-chargers', 'phi ladelphia-eagles', 'san-francisco-49ers']
    def convert_name_web_to_view(self, name):
        return name.title().replace('-', ' ')

class pga_db():
    """Makes a new database for pga"""

    db_name = "pga"
    items = ['Dustin\xa0Johnson', 'Rory\xa0McIlroy', 'Jason\xa0Day', 'Sergio\xa0Garcia',\
    'Jordan\xa0Spieth', 'Rickie\xa0Fowler', 'Justin\xa0Rose', 'Adam\xa0Scott', 'Paul\xa0Casey',\
    'Matt\xa0Kuchar', 'Kevin\xa0Kisner', 'Phil\xa0Mickelson']
    def convert_name_web_to_view(self, name):
        return name.replace('\xa0', ' ')