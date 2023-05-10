import json
import os
from flask import jsonify, Request
from tinydb import TinyDB, Query, where, operations
from datetime import datetime
import csv
import time
import re
import random
import urllib.request
import json
import pprint

my_dir = os.path.dirname(__file__)
sorted_json_file_path = os.path.join(my_dir, r'database/sorted_db.json')

sorted_database = TinyDB(sorted_json_file_path)


def get_all_movies(query):
    # pprint.pprint(query)
    filtered = filter_movies(query)
    organized = organize(filtered, query)
    culled = cull_max_page(organized, query['extra_settings']['max_movies'])
    return organized


def filter_movies(query):
    # output
    filtered_movies = {}
    sorted_movies = {}
    # print(query)

    # return all if empty query
    if not query:
        return sorted_database.table('movies').all()

    rating_filters = query['rating']['filter']
    length_filters = query['length']['filter']
    genre_filters = query['genre']['filter']
    region_filters = query['region']['filter']
    format_filters = query['format']['filter']
    type_filters = query['type']['filter']
    searchbar_filters = query['search_bar']

    rating_query = ~Query().doc_id.exists()
    length_query = ~Query().doc_id.exists()
    genre_query = ~Query().doc_id.exists()
    region_query = ~Query().doc_id.exists()
    format_query = ~Query().doc_id.exists()
    type_query = ~Query().doc_id.exists()
    searchbar_query = ~Query().doc_id.exists()

    # filter type
    for type_filter in type_filters:
        match type_filter:
            case "Movie":
                type_query = Query().media_type == "movie"

            case "Tv-series":
                type_query = Query().media_type == "tv"

            # case "Anime":
            #     type_query = Query().media_type == "anime"

            case "Documentary":
                type_query = Query().genres.any("Documentary")

    # filter format
    for format_filter in format_filters:
        match format_filter:
            case "Live-action":
                format_query = ~Query().genres.any("Animation")

            case "Animated":
                format_query = Query().genres.any("Animation")

    # filter region
    for region_filter in region_filters:
        match region_filter:
            case "western":
                region_query = ~Query().region.any("asian")

            case "asian":
                region_query = Query().region.any("western")

    # filter genre
    if len(genre_filters) > 0:
        genre_query = Query().genres.all(genre_filters)

    #  filter rating
    if len(rating_filters) > 0:
        rating_query = Query().my_rating.any(rating_filters)

    # filter length
    for length_filter in length_filters:
        match length_filter:
            case "0":
                length_query = Query().runtime <= 60
            case "1":
                length_query = Query().runtime <= 120
            case "2":
                length_query = 120 < Query().runtime < 180
            case "3":
                length_query = Query().runtime >= 180

    # filter searchbar
    # print(searchbar_filters)
    if len(searchbar_filters) > 0:
        searchbar_query = Query().title.test(lambda val: re.search(searchbar_filters, val, re.IGNORECASE))

    #  apply queries
    return sorted_database.table('movies').search(
        type_query &
        format_query &
        region_query &
        genre_query &
        rating_query &
        length_query &
        searchbar_query
    )


def organize(movies, query):
    seed = query['extra_settings']['session_seed']
    # print(query['sort'])

    def organize_rating(arr):
        return [mov for mov in arr if mov['my_rating'] == str(rank)]

    def organize_avg_rating(arr):
        # print('average rating')
        arr = sorted(arr, key=lambda k: k['vote_average'])
        arr.reverse()
        return arr

    def organize_date_rated(arr):
        arr = sorted(arr, key=lambda k: datetime.strptime(k['date_rated'], '%Y-%m-%d'))
        arr.reverse()
        return arr

    ranked = {}
    if len(movies) < 1:
        return ranked

    for rank in range(1, 10):
        temp = organize_rating(movies)

        match query['sort']['filter'][0]:
            case '0':
                temp = organize_avg_rating(temp)
            case '1':
                temp = organize_date_rated(temp)

        ranked[f'rank_{rank}'] = temp
        random.Random(seed).shuffle(ranked[f'rank_{rank}'])

    return ranked


def cull_max_page(movies, max_cull):
    max_movies = max_cull
    curr_movie = 0
    culled_movies = {}

    # print(movies)

    for rank in reversed(movies):

        if rank not in culled_movies:
            culled_movies[rank] = []

        for mov in movies[rank]:
            # pprint.pprint(mov)
            culled_movies[rank].append(mov)
            curr_movie += 1

            if curr_movie >= max_movies:
                break

        if curr_movie >= max_movies:
            break

    return culled_movies


def edit_movie(query):
    # print('query', query)
    old_data = query['oldData']
    new_data = query['newData']

    title_query = Query().id == int(old_data['id'])
    sorted_database.table('movies').update(new_data, title_query)


def add_movie(data):
    if check_dupe({'text': data['title']}):
        sorted_database.table('movies').insert(data)
    else:
        print('movie already found! not added')


def del_movie(data):
    sorted_database.table('movies').remove(Query().id == int(data['id']))


def get_all_presets():
    presets = (sorted_database.table('tag_presets').all())
    sorted_presets = sorted(presets, key=lambda d: d['tier'])
    return sorted_presets


def add_preset(data):
    sorted_database.table('tag_presets').insert(data)


def del_preset(data):
    sorted_database.table('tag_presets').remove(Query().name == str(data['name']))


def check_dupe(data):
    title_query = Query().title == str(data['text'])
    entries = sorted_database.table('movies').search(title_query)

    if len(entries) > 0:
        state = True
    else:
        state = False

    # print(state, " - ", data['text'])
    return state
