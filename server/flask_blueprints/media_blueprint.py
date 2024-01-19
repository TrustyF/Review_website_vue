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
from data_mapper.media_mapper import map_media, map_from_tmdb
from db_loader import db
from sql_models.media_model import Media, Genre, Theme, Tag, media_genre_association, media_tag_association

bp = Blueprint('media', __name__)


def get_search_category_from_type(f_media_type):
    if f_media_type in ['movie']:
        return 'movie'
    if f_media_type in ['tv', 'anime']:
        return 'tv'


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

    user_rating_sort_override = data.get('user_rating_sort_override')
    random_sort_override = data.get('random_sort_override')

    # setup query
    query = (db.session.query(Media).filter(
        or_(Media.is_deleted == 0, Media.is_deleted == None)))  # noqa

    def apply_filters(q):
        if media_type:
            q = q.filter_by(media_type=media_type)
        if search:
            if len(q.filter(Media.name.ilike(f'{search}')).all()) > 0:
                q = q.filter(Media.name.ilike(f'{search}'))

            elif len(q.filter(Media.name.ilike(f'%{search}%')).all()) > 0:
                q = q.filter(Media.name.ilike(f'%{search}%'))

            elif len(q.join(Media.genres).filter(Genre.name.ilike(f'%{search}%')).all()) > 0:
                q = q.join(Media.genres).filter(Genre.name.ilike(f'%{search}%'))

            elif len(q.join(Media.tags).filter(Tag.name.ilike(f'%{search}%')).all()) > 0:
                q = q.join(Media.tags).filter(Tag.name.ilike(f'%{search}%'))

            else:
                q = q.filter(Media.overview.ilike(f'%{search}%'))

        if genres:
            q = (q.join(Media.genres).filter(Genre.id.in_(genres))
                 .group_by(Media.id).having(func.count(Media.id) == len(genres)))
        if themes:
            q = (q.join(Media.themes).filter(Theme.id.in_(themes))
                 .group_by(Media.id).having(func.count(Media.id) == len(themes)))
        if tags:
            q = (q.join(Media.tags).filter(Tag.id.in_(tags))
                 .group_by(Media.id).having(func.count(Media.id) == len(tags)))

        if ratings:
            q = q.filter(Media.user_rating >= ratings[0],
                         Media.user_rating <= ratings[1])
        if public_ratings:
            q = q.filter(
                or_(
                    and_(Media.public_rating >= public_ratings[0],
                         Media.public_rating <= public_ratings[1]),
                    Media.public_rating.is_(None)
                )
            )

        if release_dates:
            q = q.filter(Media.release_date >= datetime(day=1, month=1, year=int(release_dates[0])),
                         Media.release_date <= datetime(day=1, month=1, year=int(release_dates[1])))
        if runtimes:
            q = q.filter(Media.runtime >= int(runtimes[0]), Media.runtime <= int(runtimes[1]))

        return q

    def order_results(q):
        # order result
        selected_ordering = None
        rating_ordering = Media.user_rating.desc() if not user_rating_sort_override else None
        rand_ordering = func.rand(session_seed) if not random_sort_override else None

        if order:
            match order:
                case 'release_date':
                    selected_ordering = Media.release_date.desc()
                case 'name':
                    selected_ordering = Media.name
                case 'public_rating':
                    selected_ordering = Media.public_rating.desc()
                case 'runtime':
                    selected_ordering = Media.runtime.desc()
                case 'date_added':
                    selected_ordering = Media.created_at.desc()

        q = q.order_by(rating_ordering, selected_ordering, Media.id)

        return q

    query = apply_filters(query)
    query = order_results(query)

    print(len(query.all()))

    # limiting
    if limit is not None:
        query = query.limit(limit).offset(page * limit)

    # get query and map
    media = query.all()
    mapped_media = map_media(media, media_type)

    return mapped_media, 200


@bp.route("/find", methods=['GET'])
def find():
    media_name = request.args.get('name')
    media_type = request.args.get('type')

    print(f'searching {media_name=} {media_type=}')

    full_medias = []
    mapped_media = []

    search_category = get_search_category_from_type(media_type)

    def request_tmdb():
        all_found = []
        id_request = requests.get(
            f'https://api.themoviedb.org/3/search/{search_category}?query={media_name}&page=1', headers={
                "accept": "application/json",
                "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"}).json()

        found_ids = [x['id'] for x in id_request['results'][:5]]
        print(found_ids)

        for media_id in found_ids:
            full_info = requests.get(
                f'https://api.themoviedb.org/3/{search_category}/{media_id}?api_key={TMDB_API_KEY}'
                f'&language=en-US&append_to_response=releases,content_ratings,external_ids').json()

            all_found.append(full_info)

        return all_found

    if media_type in ['movie', 'tv', 'anime']:
        full_medias = request_tmdb()

    if len(full_medias) > 0:
        mapped_media = map_from_tmdb(full_medias, media_type, search_category)

    return mapped_media, 200


@bp.route("/add", methods=['POST'])
def add():
    data = request.get_json()
    print('add', data['name'])

    media_object = Media(**data)

    db.session.add(media_object)
    db.session.commit()
    db.session.close()

    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}


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

    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}


@bp.route("/get_image")
def get_image():
    media_id = request.args.get('id')
    media_path = request.args.get('path')

    # print(f'getting image {media_id=} {media_path=}')

    if media_path == 'null':
        return [], 404

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

    print(f'extra posters {media_name=} {media_type=} {media_external_id=}')

    search_category = get_search_category_from_type(media_type)

    def request_tmdb_posters():
        extra_request = requests.get(
            f'https://api.themoviedb.org/3/{search_category}/{media_external_id}?api_key={TMDB_API_KEY}'
            f'&language=en-US&append_to_response=credits,images&include_image_language=en,null').json()

        tmdb_link = 'https://image.tmdb.org/t/p/w500'
        concat_posters = [tmdb_link + x['file_path'] for x in extra_request['images']['posters']]

        return concat_posters

    posters = []
    if media_type in ['movie', 'tv', 'anime']:
        posters = request_tmdb_posters()

    if media_type in ['manga']:
        pass
        # mangadex_link = 'https://image.tmdb.org/t/p/w500'
        # posters = [mangadex_link + x['file_path'] for x in extra_request['images']['posters']]

    return posters, 200


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
