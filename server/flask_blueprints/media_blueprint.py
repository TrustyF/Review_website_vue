import hashlib
import json
import os.path
import time

import requests
import random
from PIL import Image
import io
from flask import Blueprint, request, send_file
from sqlalchemy import not_, and_, or_
from sqlalchemy.sql.expression import func
from datetime import datetime, timedelta
from math import ceil, floor
from youtubesearchpython import VideosSearch
from flask_blueprints.login_blueprint import requires_auth

from constants import MAIN_DIR, TMDB_ACCESS_TOKEN, TMDB_API_KEY, IGDB_CLIENT_ID, IGDB_CLIENT_SECRET
from data_mapper.media_mapper import map_from_tmdb, map_from_mangadex, map_from_igdb, map_from_youtube
from db_loader import db
from sql_models.media_model import Media, Genre, Theme, Tag, media_genre_association, media_tag_association, TierList, \
    ContentRating
from data_mapper.serializer import serialize_media, deserialize_media

bp = Blueprint('media', __name__)


def get_search_category_from_type(f_media_type):
    if f_media_type in ['movie']:
        return 'movie'
    if f_media_type in ['tv', 'anime']:
        return 'tv'


def handle_igdb_access_token(f_source):
    def request_access_token():
        # get token
        token_request = f'https://id.twitch.tv/oauth2/token'
        token_params = {
            'client_id': IGDB_CLIENT_ID,
            'client_secret': IGDB_CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }
        token_response = requests.post(token_request, params=token_params).json()
        token_response['date_added'] = datetime.now().isoformat()
        # print('requesting new token')

        return token_response

    def make_new_token():
        # print('making new token')
        f_token = request_access_token()

        with open(file_path, 'w') as outfile:
            json.dump(f_token, outfile, indent=1)

        return f_token

    token_path = os.path.join(MAIN_DIR, 'tokens')
    file_path = os.path.join(token_path, (f_source + '.json'))

    if not os.path.isdir(token_path):
        os.mkdir(token_path)

    # no file
    if not os.path.isfile(file_path):
        return make_new_token()

    # get old token
    with open(file_path, 'r') as infile:
        old_token = json.load(infile)

    # check if outdated
    token_date_added = datetime.fromisoformat(old_token['date_added'])
    token_time_diff = abs((token_date_added - datetime.now()))

    if token_time_diff.total_seconds() > old_token['expires_in']:
        # refresh token
        return make_new_token()
    else:
        # return current token
        # print('token time left',
        #       timedelta(seconds=old_token['expires_in'] - token_time_diff.total_seconds()))
        return old_token


@bp.route("/sleep_check", methods=['GET'])
def sleep_check():
    print('not sleeping', datetime.now())
    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}


@bp.route("/get", methods=['POST'])
def get():
    # start = time.time()

    # parameters
    data = request.get_json()
    # print(data)

    media_id = data.get('id')

    limit = data.get('limit')
    page = data.get('page')
    order = data.get('order')
    media_types = data.get('types')
    session_seed = data.get('session_seed')

    genres = data.get('genres')
    themes = data.get('themes')
    tags = data.get('tags')
    tier_lists = data.get('tier_lists')

    ratings = data.get('ratings')
    public_ratings = data.get('public_ratings')
    release_dates = data.get('release_dates')
    runtimes = data.get('runtimes')
    content_ratings = data.get('content_ratings')
    difficulty = data.get('difficulty')

    # print(tier_lists, media_types)
    search = data.get('search')

    user_rating_sort_override = data.get('user_rating_sort_override')
    random_sort_override = data.get('random_sort_override')

    # setup query
    query = (db.session.query(Media).filter(
        or_(Media.is_deleted == 0, Media.is_deleted == None)))  # noqa

    # return selected media
    if media_id:
        # print('getting id', media_id)
        single_media = db.session.query(Media).filter_by(id=media_id).one_or_none()
        if single_media is not None:
            return serialize_media(single_media), 200
        else:
            return json.dumps({'ok': False}), 404, {'ContentType': 'application/json'}

    def apply_filters(q):

        match = ''

        if media_types and len(media_types) > 0:
            if 'all' not in media_types:
                q = q.filter(Media.media_type.in_(media_types))

        if search:
            conditions = [
                Media.name.ilike(f'%{search}%'),
                Media.external_name.ilike(f'%{search}%'),
                Media.genres.any(Genre.name.ilike(f'%{search}%')),
                Media.tags.any(Tag.name.ilike(f'%{search}%')),
                Media.studio.ilike(f'%{search}%'),
                Media.author.ilike(f'%{search}%'),
                Media.overview.ilike(f'%{search}%'),
            ]
            matches = [
                'name',
                'original name',
                'genre',
                'tag',
                'studio',
                'author',
                'overview',
            ]

            for i, cond in enumerate(conditions):
                res = q.filter(cond).first()
                if res is not None:
                    q = q.filter(cond)
                    match = matches[i]
                    break

                if i >= len(conditions) - 1:
                    q = q.filter(cond)

        if tier_lists:
            # print(tier_lists)
            if 'all' not in tier_lists:
                q = (q.join(Media.tier_lists).filter(TierList.name.in_(tier_lists))
                     .group_by(Media.id).having(func.count(Media.id) == len(tier_lists)))

        else:
            q = q.filter(~Media.tier_lists.any())

        if genres:
            q = (q.join(Media.genres).filter(Genre.id.in_(genres))
                 .group_by(Media.id).having(func.count(Media.id) == len(genres)))
        if themes:
            q = (q.join(Media.themes).filter(Theme.id.in_(themes))
                 .group_by(Media.id).having(func.count(Media.id) == len(themes)))
        if tags:
            q = (q.join(Media.tags).filter(Tag.id.in_(tags))
                 .group_by(Media.id).having(func.count(Media.id) == len(tags)))
        if content_ratings:
            q = q.filter(or_(
                Media.content_rating_id.in_(content_ratings),
                Media.content_rating_id.is_(None),
            ))
        if difficulty:
            if 1 in difficulty:
                q = q.filter(or_(
                    Media.difficulty.in_(difficulty),
                    Media.difficulty.is_(None),
                ))
            else:
                q = q.filter(Media.difficulty.in_(difficulty))

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

        return q, match

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

        q = q.order_by(rating_ordering, selected_ordering, rand_ordering, Media.id)

        return q

    query, matched_search_field = apply_filters(query)
    query = order_results(query)

    # limiting
    if limit is not None:
        query = query.limit(limit).offset(page * limit)

    # get query and map
    media = query.all()
    serialized_media = [serialize_media(x) for x in media]

    # end = time.time()
    # print(end - start)

    return {
        'media': serialized_media,
        'matched_field': matched_search_field,
    }, 200


@bp.route("/find", methods=['GET'])
@requires_auth
def find():
    media_name = request.args.get('name')
    media_type = request.args.get('type')
    media_id = request.args.get('id')
    media_page = request.args.get('page', type=int)

    # print(f'searching {media_name=} {media_type=} {media_id=}')

    def request_tmdb():
        all_found = []
        id_request = requests.get(
            f'https://api.themoviedb.org/3/search/{media_type}?query={media_name}&page=1', headers={
                "accept": "application/json",
                "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"}).json()

        found_ids = [x['id'] for x in id_request['results'][media_page * 5:(media_page * 5) + 5]]
        # print('tmdb_ids',found_ids)

        for media_id in found_ids:
            full_info = requests.get(
                f'https://api.themoviedb.org/3/{media_type}/{media_id}?api_key={TMDB_API_KEY}'
                f'&language=en-US&append_to_response=releases,content_ratings,credits,external_ids').json()

            all_found.append(full_info)

        return all_found

    def request_mangadex():

        def find_in_relationships(data, key, value):
            for my_dict in data:
                if my_dict.get(key) == value:
                    return my_dict

        media_request = requests.get(f"https://api.mangadex.org/manga?title={media_name}"
                                     f"&limit=5&offset={media_page * 5}&includes[]=cover_art&includes"
                                     f"[]=chapter&includes[]=author"
                                     f"&order[followedCount]=desc&order[relevance]=desc&order[rating]=desc").json()

        all_found = media_request['data']

        for media in all_found:

            rel_found = find_in_relationships(media.get('relationships'), 'type', 'cover_art')
            if rel_found is None:
                continue

            path = (f"https://uploads.mangadex.org/covers/{media['id']}"
                    f"/{rel_found['attributes']['fileName']}"
                    f".512.jpg")
            statistics = requests.get(f'https://api.mangadex.org/statistics/manga/{media["id"]}').json()

            media['poster_path'] = path
            media['vote_average'] = statistics['statistics'][media['id']]['rating']['bayesian']

        # pprint(all_found)
        return all_found

    def request_igdb():  # noqa

        token = handle_igdb_access_token('igdb_token')

        title_request = f'https://api.igdb.com/v4/games'
        title_data = f'search "{media_name}"; limit 5; offset {media_page * 5};' \
                     f' fields name,release_dates.y,genres.name,themes.name,rating,total_rating' \
                     f',category,url,summary,cover.url,involved_companies.developer,involved_companies.company.name' \
                     f',age_ratings.rating,age_ratings.category;where rating != null;'
        title_headers = {
            'Client-ID': IGDB_CLIENT_ID,
            'Authorization': f"{token['token_type']} {token['access_token']}",
        }
        title_response = requests.post(title_request, data=title_data, headers=title_headers).json()

        return title_response

    def request_youtube():
        search = VideosSearch(media_name, limit=50)

        result = search.result().get('result')[media_page * 5: (media_page * 5) + 5]

        for video in result:
            # print(video['id'])
            votes = requests.get(f'https://returnyoutubedislikeapi.com/votes?videoId={video["id"]}').json()
            try:
                vote_rating = votes['likes'] / (votes['likes'] + votes['dislikes']) * 10
            except ZeroDivisionError:
                vote_rating = 0

            video['public_rating'] = vote_rating

        return result

    mapped_media = []

    if media_type in ['movie', 'tv']:
        full_medias = request_tmdb()

        if len(full_medias) > 0:
            mapped_media = map_from_tmdb(full_medias, media_type)

    elif media_type in ['manga']:
        full_medias = request_mangadex()

        if len(full_medias) > 0:
            mapped_media = map_from_mangadex(full_medias, media_type)

    elif media_type in ['game']:
        full_medias = request_igdb()

        if len(full_medias) > 0:
            mapped_media = map_from_igdb(full_medias, media_type)

    elif media_type in ['youtube']:
        full_medias = request_youtube()

        if len(full_medias) > 0:
            mapped_media = map_from_youtube(full_medias, media_type)

    serialized_media = [serialize_media(x) for x in mapped_media]

    if len(serialized_media) > 0:
        # print(serialized_media)
        return serialized_media, 200
    else:
        return json.dumps({'ok': False}), 404, {'ContentType': 'application/json'}


@bp.route("/add", methods=['POST'])
@requires_auth
def add():
    data = request.get_json()
    # print('add', data['name'])

    # pprint(data)

    exist_check = db.session.query(Media).filter(Media.external_id == data['external_id']).one_or_none()

    # cancel if already present
    if exist_check is not None:
        return json.dumps({'ok': False}), 404, {'ContentType': 'application/json'}

    media_obj = Media(**deserialize_media(data))

    # associations
    media_obj.genres = [db.session.query(Genre).filter_by(id=x['id']).one() for x in data.get('genres', [])]
    media_obj.themes = [db.session.query(Theme).filter_by(id=x['id']).one() for x in data.get('themes', [])]
    media_obj.tags = [db.session.query(Tag).filter_by(id=x['id']).one() for x in data.get('tags', [])]
    media_obj.tier_lists = [db.session.query(TierList).filter_by(id=x['id']).one() for x in data.get('tier_lists', [])]
    if data.get('content_rating').get('id'):
        media_obj.content_rating = (db.session.query(ContentRating)
                                    .filter_by(id=data.get('content_rating').get('id')).one())

    db.session.add(media_obj)
    db.session.commit()
    db.session.close()

    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}


@bp.route("/update", methods=['POST'])
@requires_auth
def update():
    # parameters
    data = request.get_json()
    # print('update', data['name'])
    # pprint.pprint(data)

    query = db.session.query(Media).filter_by(id=data['id'])

    if query.one_or_none() is None:
        return json.dumps({'ok': False}), 200, {'ContentType': 'application/json'}

    # update
    query.update(deserialize_media(data))

    # associations
    media_obj = query.one()

    media_obj.genres = [db.session.query(Genre).filter_by(id=x['id']).one() for x in data.get('genres', [])]
    media_obj.themes = [db.session.query(Theme).filter_by(id=x['id']).one() for x in data.get('themes', [])]
    media_obj.tags = [db.session.query(Tag).filter_by(id=x['id']).one() for x in data.get('tags', [])]
    media_obj.tier_lists = [db.session.query(TierList).filter_by(id=x['id']).one() for x in data.get('tier_lists', [])]
    if data.get('content_rating').get('id'):
        media_obj.content_rating = (db.session.query(ContentRating)
                                    .filter_by(id=data.get('content_rating').get('id')).one())

    db.session.commit()
    db.session.close()

    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}


@bp.route("/delete", methods=['GET'])
@requires_auth
def delete():
    # parameters
    media_id = request.args.get('id')
    # print('delete', media_id)

    db.session.query(Media).filter_by(id=media_id).delete()
    db.session.commit()
    db.session.close()

    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}


@bp.route("/get_image", methods=['GET'])
def get_image():
    media_id = request.args.get('id')
    media_path = request.args.get('path')
    media_type = request.args.get('type')

    # print(media_id, media_path, media_type)

    poster_id = hashlib.shake_256(media_path.encode("utf-8")).hexdigest(5)

    # return not found image
    if media_path in ['null', 'undefined', 'not_found']:
        return [], 200

    file_path = os.path.join(MAIN_DIR, "assets", "poster_images_caches",
                             f"{media_id}_{media_type}_{poster_id}.jpg")

    # return saved file if exists
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/jpg')

    # check if the requested image is part of a db entry and save if true
    if db.session.query(Media).filter(Media.external_id == media_id,
                                      Media.poster_path == media_path).one_or_none():

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        response = requests.get(media_path)
        # print('making poster request', media_id, media_type)

        with open(file_path, 'wb') as outfile:
            outfile.write(response.content)

    else:
        # if preview return without saving
        response = requests.get(media_path)
        return response.content

    return send_file(file_path, mimetype='image/jpg')


@bp.route("/get_extra_posters", methods=['GET'])
@requires_auth
def search_extra_posters():
    media_name = request.args.get('name')
    media_external_id = request.args.get('external_id')
    media_type = request.args.get('type')

    # print(f'extra posters {media_name=} {media_type=} {media_external_id=}')

    search_category = get_search_category_from_type(media_type)

    def request_tmdb_posters():
        extra_request = requests.get(
            f'https://api.themoviedb.org/3/{search_category}/{media_external_id}?api_key={TMDB_API_KEY}'
            f'&language=en-US&append_to_response=credits,images&include_image_language=en,null').json()

        tmdb_link = 'https://image.tmdb.org/t/p/w500'
        concat_posters = [tmdb_link + x['file_path'] for x in extra_request['images']['posters']]

        return concat_posters

    def request_mangadex_posters():
        extra_request = requests.get(f'https://api.mangadex.org/cover?limit=100&manga%5B%5D={media_external_id}').json()
        aggregated_links = []

        if extra_request.get('data') is None:
            return []

        for entry in extra_request['data']:

            if entry['attributes']['volume'] is None:
                continue

            path = (f"https://uploads.mangadex.org/covers/{media_external_id}"
                    f"/{entry['attributes']['fileName']}"
                    f".512.jpg")
            aggregated_links.append([path, entry['attributes']['volume']])

        sorted_links = sorted(aggregated_links, key=lambda x: float(x[1]))
        clean_links = [x[0] for x in sorted_links]

        return clean_links

    def request_igdb_posters():

        token = handle_igdb_access_token('igdb_token')

        cover_request = 'https://api.igdb.com/v4/artworks'
        cover_data = f'fields url, game;where game = ({media_external_id});'
        cover_headers = {
            'Client-ID': IGDB_CLIENT_ID,
            'Authorization': f"{token['token_type']} {token['access_token']}",
        }
        cover_response = requests.post(cover_request, data=cover_data, headers=cover_headers).json()
        # print(cover_response)
        clean_covers = ['https:' + x['url'].replace('t_thumb', 't_1080p') for x in cover_response]

        return clean_covers

    def request_youtube_posters():
        base = [f'https://img.youtube.com/vi/{media_external_id}/maxresdefault.jpg']
        [base.append(f'https://img.youtube.com/vi/{media_external_id}/maxres{x}.jpg') for x in range(1, 5)]
        return base

    posters = []
    if media_type in ['movie', 'tv']:
        posters = request_tmdb_posters()

    if media_type in ['manga']:
        posters = request_mangadex_posters()

    if media_type in ['game']:
        posters = request_igdb_posters()

    if media_type in ['youtube']:
        posters = request_youtube_posters()

    if len(posters) > 0:
        # print(serialized_media)
        return posters, 200
    else:
        return json.dumps({'ok': False}), 404, {'ContentType': 'application/json'}


@bp.route("/get_scroll_banner", methods=['GET'])
def get_scroll_banner():
    def make_collage(images, width, height):
        collage = Image.new("RGB", (width * len(images), height), color=(255, 255, 255, 255))
        for j, img in enumerate(images):
            width_percent = (height / float(img.size[1]))
            hsize = int((float(img.size[0]) * float(width_percent)))
            resized = img.resize((hsize, height), Image.Resampling.LANCZOS)

            size = resized.size

            left = (size[0] - width) / 2
            right = (size[0] + width) / 2

            resized = resized.crop((left, 0, right, height))
            collage.paste(resized, (j * width, 0))

        return collage

    # get list of images
    query = (db.session.query(Media).filter(
        or_(Media.is_deleted == 0, Media.is_deleted == None)))  # noqa
    query = query.filter(Media.media_type.in_(['movie', 'tv', 'anime', 'manga', 'game']))
    query = query.order_by(func.rand(time.time()))
    query = query.limit(50)

    all_entries = query.all()
    # aggregate posters
    posters = []
    for i, x in enumerate(all_entries):

        if len(posters) > 19:
            break

        path = os.path.join(MAIN_DIR, "assets", "poster_images_caches",
                            f"{x.external_id}_{x.media_type}_{hashlib.shake_256(x.poster_path.encode('utf-8')).hexdigest(5)}.jpg")

        if os.path.exists(path):
            posters.append(path)

    # make collage
    file_path = os.path.join(MAIN_DIR, "assets", "poster_images_caches")
    banner = make_collage([Image.open(os.path.join(file_path, x)) for x in posters], 500, 750)

    mem_file = io.BytesIO()
    banner.save(mem_file, 'JPEG', quality=50)
    mem_file.seek(0)

    return send_file(mem_file, mimetype='image/jpg')


@bp.route("/get_filters", methods=['POST'])
def get_filters():
    params = request.get_json()

    media_types = params.get('types')
    media_tier_lists = params.get('tier_lists')

    # print(f'getting filters for {media_types=} {media_tier_lists=}')

    genres = db.session.query(Genre)
    themes = db.session.query(Theme)
    tags = db.session.query(Tag)
    content_ratings = db.session.query(ContentRating)

    ratings = db.session.query(func.max(Media.user_rating).label('max'),
                               func.min(Media.user_rating).label('min'))
    public_ratings = db.session.query(func.max(Media.public_rating).label('max'),
                                      func.min(Media.public_rating).label('min'))
    release_dates = db.session.query(func.max(Media.release_date).label('max'),
                                     func.min(Media.release_date).label('min'))
    runtimes = db.session.query(func.max(Media.runtime).label('max'),
                                func.min(Media.runtime).label('min'))
    if media_types and len(media_types) > 0:
        genres = genres.join(Media.genres).filter(Media.media_type.in_(media_types))
        themes = themes.join(Media.themes).filter(Media.media_type.in_(media_types))
        tags = tags.join(Media.tags).filter(Media.media_type.in_(media_types))
        content_ratings = content_ratings.join(Media.content_rating).filter(Media.media_type.in_(media_types))

        ratings = ratings.filter(Media.media_type.in_(media_types))
        public_ratings = public_ratings.filter(Media.media_type.in_(media_types))
        release_dates = release_dates.filter(Media.media_type.in_(media_types))
        runtimes = runtimes.filter(Media.media_type.in_(media_types))

    if media_tier_lists:
        genres = genres.join(Media.tier_lists).filter(TierList.name.in_(media_tier_lists))
        themes = themes.join(Media.tier_lists).filter(TierList.name.in_(media_tier_lists))
        tags = tags.join(Media.tier_lists).filter(TierList.name.in_(media_tier_lists))
        content_ratings = content_ratings.join(Media.tier_lists).filter(TierList.name.in_(media_tier_lists))

        ratings = ratings.join(Media.tier_lists).filter(TierList.name.in_(media_tier_lists))
        public_ratings = public_ratings.join(Media.tier_lists).filter(TierList.name.in_(media_tier_lists))
        release_dates = release_dates.join(Media.tier_lists).filter(TierList.name.in_(media_tier_lists))
        runtimes = runtimes.join(Media.tier_lists).filter(TierList.name.in_(media_tier_lists))

    ratings = ratings.one()
    public_ratings = public_ratings.one()
    release_dates = release_dates.one()
    runtimes = runtimes.one()

    result = {
        'genres': genres.group_by(Genre.id).all(),
        'themes': themes.group_by(Theme.id).all(),
        'tags': tags.group_by(Tag.id).all(),
        'content_ratings': content_ratings.group_by(ContentRating.id).all(),
        'all_content_ratings': db.session.query(ContentRating).all(),
        'user_ratings': [ratings.min or 0, ratings.max or 0],
        'public_ratings': [floor(public_ratings.min or 0), ceil(public_ratings.max or 0)],
        'release_dates': [release_dates.min.year, release_dates.max.year]
        if release_dates.max is not None else [0, 0],
        'runtimes': [0, ceil(runtimes.max / 15) * 15] if runtimes.max else [0, 0],
    }

    # pprint(result)

    return result, 200


@bp.route("/get_stats", methods=['GET'])
def get_stats():
    def construct_rating_list(arr):
        base = [x for x in range(1, 11)]
        types = set([x[0] for x in arr])

        constructed = {}

        for rating in base:
            for med_type in types:

                if med_type not in constructed:
                    constructed[med_type] = {}

                constructed[med_type][rating] = 0

                for entry in arr:
                    if entry[1] is None:
                        continue

                    if (entry[1]) <= (rating + 0.5) and entry[1] >= (rating - 0.5) and entry[0] == med_type:
                        constructed[med_type][rating] += entry[2]
                        continue

        return constructed

    def construct_release_date_list(arr):
        all_dates = [x[2] for x in arr]
        min_date, max_date = min(all_dates), max(all_dates)
        base = [x for x in range(min_date, max_date)]
        types = set([x[1] for x in arr])

        constructed = {}

        for year in base:
            for med_type in types:

                if med_type not in constructed:
                    constructed[med_type] = {}

                constructed[med_type][year] = []

                for entry in arr:
                    if entry[2] == year and entry[1] == med_type:
                        constructed[med_type][year].append(entry[0])
                        continue

        return constructed

    def construct_runtime_list(arr):
        if arr is None:
            return []

        time_interval = 5
        all_runtimes = [x[1] for x in arr if x[1] is not None]
        min_run, max_run = min(all_runtimes), max(all_runtimes)

        base = [x for x in range(0, max_run + time_interval) if x % time_interval == 0]
        types = set([x[0] for x in arr])

        constructed = {}

        for time in base:
            for med_type in types:

                if med_type not in constructed.keys():
                    constructed[med_type] = {}

                constructed[med_type][time] = []

                for entry in arr:
                    if entry[1] is None:
                        continue

                    if entry[1] <= time and entry[1] >= (time - time_interval) and entry[0] == med_type:
                        # if entry[0] == 'movie':
                        #     print(entry)

                        constructed[med_type][time].append(entry[2])
                        continue

        return constructed

    rating_count = (
        db.session.query(Media.media_type, Media.user_rating, func.count(Media.id).label('count'))
        .filter(Media.is_deleted.is_(None))
        .group_by(Media.media_type, Media.user_rating)
        .all()
    )

    public_rating_count = (
        db.session.query(Media.media_type, Media.public_rating, func.count(Media.id).label('count'))
        .filter(Media.is_deleted.is_(None))
        .group_by(Media.media_type, Media.public_rating)
        .all()
    )

    release_date_count = (
        db.session.query(Media.name, Media.media_type, func.extract('year', Media.release_date).label('release_year'))
        .filter(Media.is_deleted.is_(None))
        .group_by(Media.name, Media.media_type, 'release_year')
        .all()
    )

    avg_rating_release_date_count = (
        db.session.query(Media.user_rating, Media.media_type,
                         func.extract('year', Media.release_date).label('release_year'))
        .filter(Media.is_deleted.is_(None))
        .group_by(Media.user_rating, Media.media_type, 'release_year')
        .all()
    )

    avg_pub_rating_release_date_count = (
        db.session.query(Media.public_rating, Media.media_type,
                         func.extract('year', Media.release_date).label('release_year'))
        .filter(Media.is_deleted.is_(None))
        .group_by(Media.public_rating, Media.media_type, 'release_year')
        .all()
    )

    runtime_count = (
        db.session.query(Media.media_type, Media.runtime, Media.name, )
        .filter(Media.is_deleted.is_(None))
        .group_by(Media.media_type, Media.runtime, Media.name, )
        .all()
    )

    avg_rating_runtime_count = (
        db.session.query(Media.media_type, Media.runtime, Media.user_rating, )
        .filter(Media.is_deleted.is_(None))
        .group_by(Media.media_type, Media.runtime, Media.user_rating, )
        .all()
    )

    avg_pub_rating_runtime_count = (
        db.session.query(Media.media_type, Media.runtime, Media.public_rating, )
        .filter(Media.is_deleted.is_(None))
        .group_by(Media.media_type, Media.runtime, Media.public_rating, )
        .all()
    )

    # print(release_date_count)

    stats = {
        'ratings': construct_rating_list(rating_count),
        'public_ratings': construct_rating_list(public_rating_count),
        'release_dates': construct_release_date_list(release_date_count),
        'avg_rating_release_date': construct_release_date_list(avg_rating_release_date_count),
        'avg_pub_rating_release_date': construct_release_date_list(avg_pub_rating_release_date_count),
        'runtimes': construct_runtime_list(runtime_count),
        'avg_rating_runtimes': construct_runtime_list(avg_rating_runtime_count),
        'avg_pub_rating_runtimes': construct_runtime_list(avg_pub_rating_runtime_count),
    }

    # pprint.pprint(stats['avg_rating_release_date'])

    return stats, 200
