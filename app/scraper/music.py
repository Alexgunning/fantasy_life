"""Pull down music data"""
import datetime
import billboard
from flask_pymongo import MongoClient

FANTASY_LIFE_START_DATE = datetime.date(year=2016, month=8, day=1)

client = MongoClient()
db = client.fantasy

print("runnning")

def create_music_db():
    """Makes a new database for the nba"""
    players = db.players
    musicians = db.musicians
    musicians.drop()

    singers = ['Bruno Mars', 'Ed Sheeran', 'Kendrick Lamar', 'Future', 'Lil Uzi Vert',\
     'James Arthur', 'Julia Michaels', 'Imagine Dragons', 'Sam Hunt', 'Taylor Swift',\
     'Katy Perry', 'Justin Bieber']

    cursor = players.find()
    for singer, user in zip(singers, cursor):
        _ = musicians.insert({"associated_player_id": user['_id'], "artist": singer})

class Artist():
    """Class for storing the data of each artist"""
    def __init__(self, name):
        self.name = name
        self.top_ten = 0
        self.number_one = 0
        self.score = 0

def get_billboard_charts():
    """Get the music data for the progam"""

    musicians = db.musicians
    artists = [Artist(singer['artist']) for singer in musicians.find()]
    for singer in artists:
        print(singer.name)

    chart = billboard.ChartData('hot-100')

    #TODO CLEAN UP must be a better way to iterate through these loops
    #Iterate through charts until fantasy start date
    while True:
        #Get the top ten songs from the chart
        top_ten = chart[:10]
        #Go through all of the songs in the top ten
        #Searching for artists is complicated by songs having multiple artists
        #must search song name by artists we are looking for
        for i, song in enumerate(top_ten):
            for singer in artists:
                if singer.name in song.artist:
                    if i == 0:
                        singer.number_one += 1
                    singer.top_ten += 1

        chart_date = chart.previousDate.split('-')
        chart_datetime = datetime.date(year=int(chart_date[0]), month=int(chart_date[1]),\
        day=int(chart_date[2]))
        if chart_datetime < FANTASY_LIFE_START_DATE:
            break
        else:
            chart = billboard.ChartData('hot-100', date=chart.previousDate)

    for singer in artists:
        singer.score = (singer.number_one * 2) + singer.top_ten

    for singer in artists:
        musicians.update_one({
            'artist': singer.name
            }, {
                '$set': {
                    'number_one': singer.number_one,
                    'top_ten': singer.top_ten,
                    'score': singer.score
                }
            })

create_music_db()
get_billboard_charts()
