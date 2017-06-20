"""Get movie data"""
import datetime
import requests

FANTASY_LIFE_START_DATE = datetime.date(year=2016, month=8, day=1)
CURRENT_DATE = datetime.date.today()

def get_actor_movies():
    """Get the name of he movies the actor has been in for the year"""
    query = "https://api.themoviedb.org/3/person/500/movie_credits?api_key="\
    +"9a45c028490face328e53d83033a2795&language=en-US"

    res = requests.get(query)
    all_movies = res.json()['cast']

    current_movies = []
    for movie in all_movies:
        date_list = movie["release_date"].split('-')
        movie_release_date = datetime.date(year=int(date_list[0]), month=int(date_list[1]),\
        day=int(date_list[2]))
        if movie_release_date > FANTASY_LIFE_START_DATE and movie_release_date < CURRENT_DATE:
            current_movies.append(movie)
    return current_movies
