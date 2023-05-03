import json
import os
from flask import jsonify, Request
from tinydb import TinyDB, Query, where
from datetime import datetime
import csv

my_dir = os.path.dirname(__file__)
sorted_json_file_path = os.path.join(my_dir, r'database/sorted_db.json')

sorted_database = TinyDB(sorted_json_file_path)


def get_all_movies(query):
    filtered_movies = filter_movies(query)
    return filtered_movies


def filter_movies(query):
    # output
    filtered_movies = {}
    sorted_movies = {}
    # print(query)

    # return all if empty query
    if not query:
        for rank in range(1, 11):
            filtered_movies[f'ranked_{rank}'] = sorted_database.table(f'ranked_{rank}').all()

        return filtered_movies

    rating_filters = query['rating']['filter']
    length_filters = query['length']['filter']
    genre_filters = query['genre']['filter']
    region_filters = query['region']['filter']
    format_filters = query['format']['filter']
    type_filters = query['type']['filter']
    date_rated_filters = query['date_rated']['filter']

    rating_query = ~Query().doc_id.exists()
    length_query = ~Query().doc_id.exists()
    genre_query = ~Query().doc_id.exists()
    region_query = ~Query().doc_id.exists()
    format_query = ~Query().doc_id.exists()
    type_query = ~Query().doc_id.exists()
    date_rated_query = ~Query().doc_id.exists()

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

    #  loop over ranks and apply queries
    for rank in range(1, 11):
        filtered_movies[f'ranked_{rank}'] = sorted_database.table(f'ranked_{rank}').search(
            type_query &
            format_query &
            region_query &
            genre_query &
            rating_query &
            length_query
        )

        # # apply sorting
        # sorted_movies[f'ranked_{rank}'] = sorted(filtered_movies,
        #                                          key=lambda x: datetime.strptime(x['date_rated'], '%y-%m-%d'))

    return filtered_movies


def edit_movie(query):
    # print(query)
    old_data = query['oldData']
    new_data = query['newData']

    curr_table = f'ranked_{old_data["my_rating"]}'
    title_query = Query().title == str(old_data['title'])

    element = sorted_database.table(curr_table).get(title_query)

    print('updated')
    sorted_database.table(curr_table).update(new_data, title_query)
    print(sorted_database.table(curr_table).get(title_query))

    if "my_rating" in new_data:
        print('changed tables')
        target_table = f'ranked_{new_data["my_rating"]}'

        try:
            sorted_database.table(target_table).insert(element)
        except ValueError:
            print('already in table')
        sorted_database.table(curr_table).remove(title_query)


