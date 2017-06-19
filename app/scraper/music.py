"""Pull down music data"""
import requests
import billboard
import datetime
from flask_pymongo import MongoClient

FANTASY_LIFE_START_DATE = datetime.date(year=2016, month=8, day=1)

client = MongoClient()
db = client.fantasy

print("runnning")

def create_music_db():
    """Makes a new database for the nba"""
    players = db.players
    musicians = db.musicians

    artists = ['Bruno Mars', 'Ed Sheeran', 'Kendrick Lamar', 'Future', 'Lil Uzi Vert',\
     'James Arthur', 'Julia Michaels', 'Imagine Dragons', 'Sam Hunt', 'Childish Gambino',\
     'Shawn Mende s', 'Brett Young']

    cursor = players.find()
    for artist, document in zip(artists, cursor):
        _ = musicians.insert({"_id": document['_id'], "artist": artist})


def get_billboard_charts():
    """Get the music data for the progam"""
    chart = billboard.ChartData('hot-100')
    print(chart.date)
    print(type(chart.date))
    chart_date = chart.date.split('-')
    chart_datetime = datetime.date(year=int(chart_date[0]), month=int(chart_date[1]),\
    day=int(chart_date[2]))
    print(chart_datetime)
    print(type(chart_datetime))
    prev = chart.previousDate
    print(prev)

    for i in range(20):
        song = chart[i]  # Get no. 1 song on chart
        # print(song.artist)

# create_music_db()
get_billboard_charts()
