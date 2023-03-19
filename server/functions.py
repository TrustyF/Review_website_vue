import json
from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage, MemoryStorage
from tinydb.middlewares import CachingMiddleware
from pprint import pprint

unsorted_database = TinyDB('database/unsorted_db.json')


# sorted_database = TinyDB('database/sorted_db.json')


def get_all_movies():
    # create table by rating
    sorted_movies = []
    for i in reversed(range(1, 11)):
        # get rating
        records = unsorted_database.search(where('my_rating') == str(i))
        # sort by vote avg
        sorted_records = sorted(records, key=lambda d: d['vote_average'], reverse=True)
        sorted_movies.append(sorted_records)

    return sorted_movies


def edit_movie(query):
    unsorted_database.update(query, where('title') == query['title'])


def load_init():
    print('loading init')
    with open('../client/public/assets/movie_db_lib.json', 'rb') as infile:
        data = json.load(infile)

    for entry in data:
        unsorted_database.insert(entry)
