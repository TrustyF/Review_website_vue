import json
import os
from flask import jsonify, Request
from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage, MemoryStorage
from tinydb.middlewares import CachingMiddleware
from pprint import pprint

my_dir = os.path.dirname(__file__)
sorted_json_file_path = os.path.join(my_dir, r'database\sorted_db.json')

sorted_database = TinyDB(sorted_json_file_path)


# def init_sorted():
#     def load_init():
#         print('loading init')
#         with open('../client/public/assets/movie_db_lib.json', 'rb') as infile:
#             data = json.load(infile)
#
#         for entry in data:
#             unsorted_database.insert(entry)
#
#     unsorted_database = TinyDB(unsorted_json_file_path)
#     for i in reversed(range(1, 11)):
#         curr_table = sorted_database.table(f'ranked_{i}')
#         records = unsorted_database.search(where('my_rating') == str(i))
#         curr_table.insert_multiple(records)


def get_all_movies(query):
    print('getting movies!!')
    filtered_movies = filter_movies(query)
    return filtered_movies


def filter_movies(query):
    rating_filters = query['rating']['filter']
    length_filters = query['length']['filter']
    genre_filters = query['genre']['filter']
    format_filters = query['format']['filter']
    type_filters = query['type']['filter']

    rating_query = ~Query().doc_id.exists()
    length_query = ~Query().doc_id.exists()
    genre_query = ~Query().doc_id.exists()
    format_query = ~Query().doc_id.exists()
    type_query = ~Query().doc_id.exists()

    # filter type
    for type_filter in type_filters:
        match type_filter:
            case "Movie":
                type_query = Query().media_type == "movie"

            case "Tv-series":
                type_query = Query().media_type == "tv"

            case "Documentary":
                type_query = Query().genres.any("Documentary")

    # filter format
    for format_filter in format_filters:
        match format_filter:
            case "Live-action":
                format_query = ~Query().genres.any("Animation")

            case "Animated":
                format_query = Query().genres.any("Animation")

    # filter genre
    if len(genre_filters) > 0:
        genre_query = Query().genres.all(genre_filters)

    #  filter rating
    if len(rating_filters) > 0:
        rating_query = Query().my_rating.any(rating_filters)

    # filter length
    for length_filter in length_filters:
        match length_filter:
            case "1":
                length_query = Query().runtime <= 120
            case "2":
                length_query = 120 < Query().runtime < 180
            case "3":
                length_query = Query().runtime >= 180

    # output
    filtered_movies = {}

    #  loop over ranks and apply queries
    for rank in range(1, 11):
        print('test', sorted_database.table(f'ranked_{rank}'))
        filtered_movies[f'ranked_{rank}'] = sorted_database.table(f'ranked_{rank}').search(
            type_query &
            format_query &
            genre_query &
            rating_query &
            length_query
        )
    print('returning filtered!')
    return filtered_movies

# def edit_movie(query):
#     unsorted_database.update(query, where('title') == query['title'])
