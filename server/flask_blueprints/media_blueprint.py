import io
import json
import os.path
from pprint import pprint
import requests

from flask import Blueprint, request, Response, jsonify, send_file
from sqlalchemy.sql.expression import func

from constants import MAIN_DIR, TMDB_ACCESS_TOKEN, TMDB_API_KEY
from data_mapper.media_mapper import map_media
from db_loader import db
from sql_models.media_model import Media, Genre, Theme, Tag, media_genre_association

bp = Blueprint('media', __name__)


@bp.route("/get")
def get():
    # parameters
    limit = request.args.get('limit', type=int)
    page = request.args.get('page', type=int)
    order = request.args.get('order')
    media_type = request.args.get('type')
    session_seed = request.args.get('session_seed', type=int)

    genres = request.form.getlist('genres', type=int)

    print(f'{genres=}')

    print(f'{limit =}', f'{order =}', f'{page =}', f'{media_type =}', f'{session_seed =}')

    # setup query
    query = (
        db.session.query(Media)
        .filter_by(media_type=media_type)
    )

    # order result
    match order:
        case 'release_date':
            query = query.order_by(Media.user_rating.desc(),
                                   Media.release_date.desc(),
                                   func.rand(session_seed),
                                   Media.id)
        case 'name':
            query = query.order_by(Media.user_rating.desc(),
                                   Media.name, func.rand(session_seed),
                                   Media.id)
        case _:
            query = query.order_by(Media.user_rating.desc(),
                                   func.rand(session_seed),
                                   Media.id)

    #     query = query.join(Card).order_by(Card.card_price.desc())
    #     query = query.join(CardTemplate).order_by(UserCard.storage_id, CARD_TYPE_PRIORITY, CardTemplate.name)

    # limiting
    if limit is not None:
        query = query.limit(limit).offset(page * limit)

    # get query and map
    media = query.all()
    mapped_media = map_media(media, media_type=media_type)

    return mapped_media, 200


@bp.route("/get_image")
def get_image():
    media_id = request.args.get('id')
    file_path = os.path.join(MAIN_DIR, "assets", "poster_images_caches", f"{media_id}.jpg")

    # download locally if it doesn't exist
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        matched_media = db.session.query(Media).filter_by(id=media_id).one()
        response = requests.get(matched_media.poster_path)

        with open(file_path, 'wb') as outfile:
            outfile.write(response.content)

    return send_file(file_path, mimetype='image/jpg')


@bp.route("/get_extra_posters")
def search_extra_posters():
    media_id = request.args.get('id')
    media_type = request.args.get('type')

    print(f'extra posters {media_id=} {media_type=}')

    req = f'https://api.themoviedb.org/3/find/{media_id}?external_source=imdb_id'
    headers = {
        "accept": "application/json",
        "Authorization": 'Bearer ' + TMDB_ACCESS_TOKEN
    }

    response = requests.get(req, headers=headers).json()
    simple_data = response[f'{media_type}_results'][0]

    extra_request = f'https://api.themoviedb.org/3/{media_type}/{simple_data["id"]}?api_key={TMDB_API_KEY}' \
                    f'&language=en-US&append_to_response=credits,images&include_image_language=en,null'
    full_data = requests.get(extra_request).json()

    posters = [x['file_path'] for x in full_data['images']['posters']]

    return posters


@bp.route("/get_filters")
def get_filters():
    media_type = request.args.get('type')

    print(f'getting filters for {media_type=}')

    genres = (db.session.query(Genre).join(Media.genres)
              .filter(Media.media_type == media_type).distinct().all())
    themes = (db.session.query(Theme).join(Media.themes)
              .filter(Media.media_type == media_type).distinct().all())
    tags = (db.session.query(Tag).join(Media.tags)
            .filter(Media.media_type == media_type).distinct().all())

    result = {
        'genres': genres,
        'themes': themes,
        'tags': tags,
    }

    return result, 200
