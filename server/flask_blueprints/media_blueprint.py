import io
import json
import os.path
from pprint import pprint
import requests

from flask import Blueprint, request, Response, jsonify, send_file
from sqlalchemy import not_, and_, or_
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql.expression import func
from datetime import datetime
from math import ceil, floor

from constants import MAIN_DIR, TMDB_ACCESS_TOKEN, TMDB_API_KEY
from data_mapper.media_mapper import map_media
from db_loader import db
from sql_models.media_model import Media, Genre, Theme, Tag, media_genre_association, media_tag_association

bp = Blueprint('media', __name__)


@bp.route("/get", methods=['POST'])
def get():
    # parameters
    data = request.get_json()
    print(data)
    limit = data.get('limit')
    page = data.get('page')
    order = data.get('order')
    media_type = data.get('type')
    session_seed = data.get('session_seed')

    genres = data.get('genres')
    themes = data.get('themes')
    tags = data.get('tags')
    ratings = data.get('ratings')
    public_ratings = data.get('public_ratings')
    release_dates = data.get('release_dates')
    runtimes = data.get('runtimes')

    search = data.get('search')

    # setup query
    query = db.session.query(Media)

    if media_type:
        query = query.filter_by(media_type=media_type)

    # apply filters
    if search:
        if len(query.filter(Media.name.ilike(f'%{search}%')).all()) > 0:
            query = query.filter(Media.name.ilike(f'%{search}%'))

        elif len(query.join(Media.genres).filter(Genre.name.ilike(f'%{search}%')).all()) > 0:
            query = query.join(Media.genres).filter(Genre.name.ilike(f'%{search}%'))

        elif len(query.join(Media.tags).filter(Tag.name.ilike(f'%{search}%')).all()) > 0:
            query = query.join(Media.tags).filter(Tag.name.ilike(f'%{search}%'))

        else:
            query = query.filter(Media.overview.ilike(f'%{search}%'))

    if genres:
        query = (query.join(Media.genres).filter(Genre.id.in_(genres))
                 .group_by(Media.id).having(func.count(Media.id) == len(genres)))
    if themes:
        query = (query.join(Media.themes).filter(Theme.id.in_(themes))
                 .group_by(Media.id).having(func.count(Media.id) == len(themes)))
    if tags:
        query = (query.join(Media.tags).filter(Tag.id.in_(tags))
                 .group_by(Media.id).having(func.count(Media.id) == len(tags)))

    if ratings:
        query = query.filter(Media.user_rating >= ratings[0],
                             Media.user_rating <= ratings[1])
    if public_ratings:
        query = query.filter(
            or_(
                and_(Media.public_rating >= public_ratings[0],
                     Media.public_rating <= public_ratings[1]),
                Media.public_rating.is_(None)
            )
        )

    if release_dates:
        query = query.filter(Media.release_date >= datetime(day=1, month=1, year=int(release_dates[0])),
                             Media.release_date <= datetime(day=1, month=1, year=int(release_dates[1])))
    if runtimes:
        query = query.filter(Media.runtime >= int(runtimes[0]), Media.runtime <= int(runtimes[1]))

    print(len(query.all()))

    # order result
    match order:
        case 'release_date':
            query = query.order_by(Media.user_rating.desc(),
                                   Media.release_date.desc(),
                                   func.rand(session_seed))
        case 'name':
            query = query.order_by(Media.user_rating.desc(),
                                   Media.name, func.rand(session_seed))
        case _:
            query = query.order_by(Media.user_rating.desc(),
                                   func.rand(session_seed))

    # limiting
    if limit is not None:
        query = query.limit(limit).offset(page * limit)

    # get query and map
    media = query.all()
    mapped_media = map_media(media)

    return mapped_media, 200


@bp.route("/update", methods=['POST'])
def update():
    # parameters
    data = request.get_json()
    print('update', data)

    media_id = data.get('id')
    del data['id']

    db.session.query(Media).filter_by(id=media_id).update(data)
    db.session.commit()
    db.session.close()

    return [], 200


@bp.route("/get_image")
def get_image():

    media_id = request.args.get('id')
    media_path = request.args.get('path')

    print(f'getting image {media_id=} {media_path=}')

    image_id = media_path.split('/')[-1]
    file_path = os.path.join(MAIN_DIR, "assets", "poster_images_caches", image_id)

    # # download locally if it doesn't exist
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        response = requests.get(media_path)

        with open(file_path, 'wb') as outfile:
            outfile.write(response.content)

    return send_file(file_path, mimetype='image/jpg')


@bp.route("/get_extra_posters")
def search_extra_posters():
    media_name = request.args.get('name')
    media_external_id = request.args.get('external_id')
    media_type = request.args.get('type')

    print(f'extra posters {media_name=} {media_type=}')
    posters = []

    if media_type == 'movie':
        # name_formatted = media_name.replace(' ', '%20')
        #
        # req = f'https://api.themoviedb.org/3/search/{media_type}?query={name_formatted}&include_adult=true&page=1'
        # headers = {"accept": "application/json", "Authorization": 'Bearer ' + TMDB_ACCESS_TOKEN}
        #
        # response = requests.get(req, headers=headers).json()
        # simple_data = response['results'][0]
        #
        # extra_request = f'https://api.themoviedb.org/3/{media_type}/{simple_data["id"]}?api_key={TMDB_API_KEY}' \
        #                 f'&language=en-US&append_to_response=credits,images&include_image_language=en,null'

        extra_request = f'https://api.themoviedb.org/3/{media_type}/{media_external_id}?api_key={TMDB_API_KEY}' \
                        f'&language=en-US&append_to_response=credits,images&include_image_language=en,null'

        full_data = requests.get(extra_request).json()
        tmdb_link = 'https://image.tmdb.org/t/p/w500'
        posters = [tmdb_link + x['file_path'] for x in full_data['images']['posters']]

    return posters


@bp.route("/get_filters")
def get_filters():
    media_type = request.args.get('type')

    print(f'getting filters for {media_type=}')

    genres = db.session.query(Genre).join(Media.genres)

    themes = db.session.query(Theme).join(Media.themes)

    tags = (db.session.query(Tag)
            .join(Media.tags)
            .order_by(Tag.image_path))

    ratings = (db.session.query(func.max(Media.user_rating).label('max'),
                                func.min(Media.user_rating).label('min'))
               .filter(Media.user_rating.is_not(None)))

    public_ratings = db.session.query(func.max(Media.public_rating).label('max'),
                                      func.min(Media.public_rating).label('min')).filter(
        Media.public_rating != 0, Media.public_rating.is_not(None))

    release_dates = (db.session.query(func.max(Media.release_date).label('max'),
                                      func.min(Media.release_date).label('min'))
                     .filter(Media.release_date.is_not(None)))

    runtimes = (db.session.query(func.max(Media.runtime).label('max'),
                                 func.min(Media.runtime).label('min'))
                .filter(Media.runtime.is_not(None)))

    if media_type:
        genres = genres.filter(Media.media_type == media_type)
        themes = themes.filter(Media.media_type == media_type)
        tags = tags.filter(Media.media_type == media_type)
        ratings = ratings.filter(Media.media_type == media_type)
        public_ratings = public_ratings.filter(Media.media_type == media_type)
        release_dates = release_dates.filter(Media.media_type == media_type)
        runtimes = runtimes.filter(Media.media_type == media_type)

    ratings = ratings.one()
    public_ratings = public_ratings.one()
    release_dates = release_dates.one()
    runtimes = runtimes.one()

    # print(ratings, public_ratings, release_dates, runtimes)

    result = {
        'genres': genres.all(),
        'themes': themes.all(),
        'tags': tags.all(),
        'user_ratings': [ratings.min or 0, ratings.max or 0],
        'public_ratings': [floor(public_ratings.min or 0), ceil(public_ratings.max or 0)],
        'release_dates': [release_dates.min.year, release_dates.max.year],
        'runtimes': [0, ceil(runtimes.max / 15) * 15] if runtimes.max else [0, 0],
    }

    return result, 200
