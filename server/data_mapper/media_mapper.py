import datetime
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


def map_media(medias):
    mapped_medias = []

    pub_rating_min = (db.session.query(func.min(Media.public_rating))
                      .where(Media.public_rating > 0)
                      .scalar())
    pub_rating_max = (db.session.query(func.max(Media.public_rating))
                      .scalar())
    user_rating_min = (db.session.query(func.min(Media.user_rating))
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
            if (pub_rating_min <= 5 if pub_rating_min is not None else False) else entry.public_rating

        mapped['genres'] = jsonify(entry.genres).json if entry.genres else None
        mapped['themes'] = jsonify(entry.themes).json if entry.themes else None
        mapped['tags'] = jsonify(entry.tags).json if entry.tags else None

        mapped_medias.append(mapped)

    return mapped_medias


def map_from_tmdb(medias, media_type):
    mapped_medias = []

    for entry in medias:
        content_rating = [x for x in entry['releases']['countries']
                          if x['iso_3166_1'] == 'US'
                          or x['iso_3166_1'] == 'JP']

        mapping = {
            'name': entry.get('title'),
            'release_date': entry.get('release_date'),
            'overview': entry.get('overview'),
            'poster_path': ('https://image.tmdb.org/t/p/w500' + entry.get('poster_path'))
            if entry.get('poster_path') else None,
            'media_type': media_type,
            'user_rating': 0,
            'public_rating': entry.get('vote_average'),
            'external_id': entry.get('imdb_id'),
            'runtime': entry.get('runtime'),
            # 'content_rating': entry['releases']['countries'].get('certification')
            'content_rating': content_rating[0].get('certification') if len(content_rating) > 0 else None
        }

        media_object = Media(**mapping)
        mapped_medias.append(media_object)

    return mapped_medias
