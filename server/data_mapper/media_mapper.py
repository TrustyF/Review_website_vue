import datetime
import json
from pprint import pprint
import time

from db_loader import db
from sql_models.media_model import Media, Genre
from sqlalchemy import func
from flask import jsonify


def remap_value(value, old_min, old_max, new_min, new_max):
    if None in (value, old_min, old_max, new_min, new_max):
        return 0

    if value < old_min:
        return value
    if value > old_max:
        return value

    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    new_value = (((value - old_min) * new_range) / old_range) + new_min
    return new_value


def map_media(medias, media_type):
    mapped_medias = []

    pub_rating_min = (db.session.query(func.min(Media.public_rating))
                      .where(Media.media_type == media_type)
                      .where(Media.public_rating > 0)
                      .scalar())
    pub_rating_max = (db.session.query(func.max(Media.public_rating))
                      .where(Media.media_type == media_type)
                      .scalar())
    user_rating_min = (db.session.query(func.min(Media.user_rating))
                       .where(Media.media_type == media_type)
                       .scalar())

    user_rating_max = 10

    # insert queried values and associations
    for entry in medias:
        mapped = jsonify(entry).json

        mapped['release_date'] = entry.release_date.isoformat() if entry.release_date else None

        # remap public rating to match my rating better, unless the min max range is too small, default to unmapped
        mapped['scaled_public_rating'] = remap_value(entry.public_rating,
                                                     pub_rating_min,
                                                     pub_rating_max,
                                                     user_rating_min,
                                                     user_rating_max) \
            if (pub_rating_min <= 7 if pub_rating_min is not None else False) else entry.public_rating

        mapped['genres'] = jsonify(entry.genres).json if entry.genres else None
        mapped['themes'] = jsonify(entry.themes).json if entry.themes else None
        mapped['tags'] = jsonify(entry.tags).json if entry.tags else None

        mapped_medias.append(mapped)

    return mapped_medias


def map_from_tmdb(medias, media_type, search_category):
    def mapping_tmdb_movie(entry):
        content_rating = ''
        if 'releases' in entry:
            for x in entry['releases']['countries']:
                if x['iso_3166_1'] == 'US' or x['iso_3166_1'] == 'JP':
                    content_rating = x.get('certification')

        movie_mapping = {
            'name': entry.get('title'),
            'release_date': entry.get('release_date'),
            'overview': entry.get('overview'),
            'poster_path': ('https://image.tmdb.org/t/p/w500' + entry.get('poster_path'))
            if entry.get('poster_path') else None,
            'media_type': media_type,
            'user_rating': 0,
            'public_rating': entry.get('vote_average'),
            'external_id': entry.get('id'),
            'runtime': entry.get('runtime'),
            'content_rating': content_rating
        }
        return movie_mapping

    def mapping_tmdb_tv(entry):

        def get_content_rating():
            def sort_func(item):
                if item[0] == 'US':
                    return 0
                elif item[0] == 'JS':
                    return 1
                else:
                    return 2

            if len(entry.get('content_ratings').get('results')) < 1:
                return

            ratings = [[x['iso_3166_1'], x['rating']] for x in entry['content_ratings']['results']]
            sorted_ratings = sorted(ratings, key=sort_func)

            return sorted_ratings[0][1]

        tv_mapping = {
            'name': entry.get('name'),
            'release_date': entry.get('first_air_date'),
            'overview': entry.get('overview'),
            'poster_path': ('https://image.tmdb.org/t/p/w500' + entry.get('poster_path'))
            if entry.get('poster_path') else None,
            'media_type': media_type,
            'user_rating': 0,
            'public_rating': entry.get('vote_average'),
            'external_id': entry.get('id'),
            'content_rating': get_content_rating(),
            'episodes': entry.get('number_of_episodes'),
            'seasons': entry.get('number_of_seasons'),
        }
        return tv_mapping

    mapped_medias = []

    for media in medias:

        mapping = {}

        if search_category in ['movie']:
            mapping = mapping_tmdb_movie(media)
        if search_category in ['tv']:
            mapping = mapping_tmdb_tv(media)

        mapped_medias.append(Media(**mapping))

    # pprint(mapped_medias[0])
    return mapped_medias


def map_from_mangadex(medias, media_type):
    mapped_medias = []

    # with open('temp.json', 'w') as outfile:
    #     json.dump(medias[0], outfile)

    for media in medias:
        attrib = media.get('attributes')
        mapping = {
            'name': attrib.get('title').get('en'),
            'release_date': f"{attrib.get('year')}-01-01",
            'overview': attrib.get('description').get('en'),
            'poster_path': media.get('poster_path'),
            'media_type': media_type,
            'user_rating': 0,
            'public_rating': media.get('vote_average'),
            'external_id': media.get('id'),
            'content_rating': attrib.get('contentRating')
        }

        mapped_medias.append(Media(**mapping))

    # pprint(mapped_medias[0])
    return mapped_medias


def map_from_igdb(medias, media_type):
    mapped_medias = []

    with open('temp.json', 'w') as outfile:
        json.dump(medias[0], outfile)

    for media in medias:
        mapping = {
            'name': media.get('name'),
            'release_date': f"{media.get('release_dates')[0].get('y')}-01-01" if media.get(
                'release_dates') else None,
            'overview': media.get('summary'),
            'poster_path': 'https:' + media.get('cover').get('url') if media.get('cover') else None,
            'media_type': media_type,
            'user_rating': 0,
            'public_rating': media.get('total_rating') / 10 if media.get('total_rating') else None,
            'external_id': media.get('id'),
            'content_rating': media.get('contentRating')
        }

        mapped_medias.append(Media(**mapping))

    return mapped_medias
