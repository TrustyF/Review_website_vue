import datetime
import pprint
import time

from db_loader import db
from sql_models.media_model import Media
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
