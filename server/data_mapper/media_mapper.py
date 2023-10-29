import datetime
import pprint
import time

from db_loader import db
from sql_models.media_model import Media
from flask import jsonify


def map_media(entry):
    mapped = jsonify(entry).json

    mapped['release_date'] = entry.release_date.isoformat()

    # mapped['public_rating'] =

    mapped['genres'] = jsonify(entry.genres).json
    mapped['themes'] = jsonify(entry.themes).json
    mapped['tags'] = jsonify(entry.tags).json

    return mapped
