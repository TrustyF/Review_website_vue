import datetime
import dateutil.parser
import json
from pprint import pprint
import time

from db_loader import db
from sql_models.media_model import Media, Genre, ContentRating, Theme
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


def write_temp(entry):
    with open('temp.json', 'w') as outfile:
        json.dump(entry, outfile)


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

        # print(entry.name if entry is not None else entry)

        mapped['release_date'] = entry.release_date.isoformat() if entry.release_date is not None else None

        # remap public rating to match my rating better, unless the min max range is too small, default to unmapped
        mapped['scaled_public_rating'] = remap_value(entry.public_rating,
                                                     pub_rating_min,
                                                     pub_rating_max,
                                                     user_rating_min,
                                                     user_rating_max) \
            if (pub_rating_min <= 7 if pub_rating_min is not None else False) else entry.public_rating

        mapped['genres'] = jsonify(entry.genres).json if entry.genres else []
        mapped['themes'] = jsonify(entry.themes).json if entry.themes else []
        mapped['tags'] = jsonify(entry.tags).json if entry.tags else []
        mapped['content_ratings'] = jsonify(entry.content_ratings).json if entry.content_ratings else None

        mapped_medias.append(mapped)

    return mapped_medias


def map_associations(table, array, media_type):
    if array is None or len(array) < 1:
        return []

    objects = []

    for val in array:

        if val == '':
            continue

        exist_check = db.session.query(table).filter(table.name == val)

        # check if instance exists, create if not
        if exist_check.one_or_none() is None:
            obj = table(name=val, origin=media_type)
            db.session.add(obj)
            db.session.commit()

        obj = exist_check.one()
        objects.append(obj)

    return objects


def map_from_tmdb(medias, media_type, search_category):
    def mapping_tmdb_movie(entry):

        def get_content_rating():
            content_rating = ''
            if 'releases' in entry:
                for x in entry['releases']['countries']:
                    if x['iso_3166_1'] == 'US' or x['iso_3166_1'] == 'JP':
                        content_rating = x.get('certification')
            return [content_rating]

        def get_genres():
            if 'genres' in entry:
                return [x['name'] for x in entry['genres']]

        def get_studio():
            if 'production_companies' in entry:
                if len(entry['production_companies']) > 0:
                    return entry.get('production_companies')[0]['name']
                else:
                    return None

        def get_author():
            if 'created_by' in entry:
                if len(entry['created_by']) > 0:
                    return entry.get('created_by')[0]['name']

            elif 'credits' in entry:
                if 'crew' in entry['credits']:
                    for crew in entry['credits']['crew']:
                        if crew.get('known_for_department') == 'Directing':
                            return crew.get('name')

        movie_mapping = {
            'name': entry.get('title'),
            'release_date': dateutil.parser.parse(entry.get('release_date')).date() if entry.get(
                'release_date') else None,
            'overview': entry.get('overview'),
            'poster_path': ('https://image.tmdb.org/t/p/w500' + entry.get('poster_path'))
            if entry.get('poster_path') else None,
            'media_type': media_type,
            'user_rating': None,
            'public_rating': entry.get('vote_average'),
            'external_id': entry.get('id'),
            'external_link': 'https://www.imdb.com/title/' + entry.get('external_ids').get('imdb_id')
            if entry.get('external_ids') and entry.get('external_ids').get('imdb_id') else None,
            'studio': get_studio(),
            'author': get_author(),
            'runtime': entry.get('runtime'),
            'content_ratings': map_associations(ContentRating, get_content_rating(), media_type),
            'genres': map_associations(Genre, get_genres(), media_type),
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

            return [sorted_ratings[0][1]]

        def get_genres():
            if 'genres' in entry:
                return [x['name'] for x in entry['genres']]

        def get_studio():
            if 'production_companies' in entry:
                if len(entry['production_companies']) > 0:
                    return entry.get('production_companies')[0]['name']
                else:
                    return None

        def get_author():
            if 'created_by' in entry:
                if len(entry['created_by']) > 0:
                    return entry.get('created_by')[0]['name']

            elif 'credits' in entry:
                if 'crew' in entry['credits']:
                    for crew in entry['credits']['crew']:
                        if crew.get('known_for_department') == 'Directing':
                            return crew.get('name')

        tv_mapping = {
            'name': entry.get('name'),
            'release_date': dateutil.parser.parse(entry.get('first_air_date')).date() if entry.get(
                'first_air_date') else None,
            'overview': entry.get('overview'),
            'poster_path': ('https://image.tmdb.org/t/p/w500' + entry.get('poster_path'))
            if entry.get('poster_path') else None,
            'media_type': media_type,
            'user_rating': None,
            'public_rating': entry.get('vote_average'),
            'external_id': entry.get('id'),
            'external_link': 'https://www.imdb.com/title/' + entry.get('external_ids').get('imdb_id')
            if entry.get('external_ids') and entry.get('external_ids').get('imdb_id') else None,
            'episodes': entry.get('number_of_episodes'),
            'seasons': entry.get('number_of_seasons'),
            'studio': get_studio(),
            'author': get_author(),
            'content_ratings': map_associations(ContentRating, get_content_rating(), media_type),
            'genres': map_associations(Genre, get_genres(), media_type),
        }
        return tv_mapping

    mapped_medias = []
    for media in medias:

        mapping = {}

        if search_category in ['movie']:
            mapping = mapping_tmdb_movie(media)
        if search_category in ['tv']:
            mapping = mapping_tmdb_tv(media)

        media_obj = Media(**mapping)
        mapped_medias.append(media_obj)

    return mapped_medias


def map_from_mangadex(medias, media_type):
    mapped_medias = []

    def get_genres(entry):
        genres = []
        if 'tags' in entry['attributes']:
            for tag in entry['attributes']['tags']:
                if tag['attributes']['group'] == 'genre':
                    if 'en' in tag['attributes']['name'].keys():
                        genres.append(tag['attributes']['name']['en'])

        return genres

        # return [x['attributes']['name']['en'] if x['attributes']['group'] == 'genre' else None for x in
        #         entry['tags']]

    def get_author(entry):
        for rel in entry['relationships']:
            if rel['type'] == 'author':
                return rel['attributes']['name']

    for media in medias:
        attrib = media.get('attributes')
        mapping = {
            'name': attrib.get('title').get('en'),
            'release_date': dateutil.parser.parse(f"{attrib.get('year')}-01-01").date() if attrib.get('year') else None,
            'overview': attrib.get('description').get('en'),
            'poster_path': media.get('poster_path'),
            'media_type': media_type,
            'user_rating': None,
            'public_rating': media.get('vote_average'),
            'external_id': media.get('id'),
            'external_link': 'https://mangadex.org/title/' + media.get('id'),
            'author': get_author(media),
            'content_ratings': map_associations(ContentRating, [attrib.get('contentRating')], media_type),
            'genres': map_associations(Genre, get_genres(media), media_type),
        }

        mapped_medias.append(Media(**mapping))

    return mapped_medias


def map_from_igdb(medias, media_type):
    mapped_medias = []

    # write_temp(medias[0])

    def get_genres(entry):
        themes = []
        if 'themes' not in entry:
            return
        for theme in entry['themes']:
            if len(entry['themes']) > 0:
                themes.append(theme['name'])

        return themes

    def get_themes(entry):
        genres = []
        if 'genres' not in entry:
            return
        for genre in entry['genres']:
            if len(entry['genres']) > 0:
                genres.append(genre['name'])

        return genres

    def get_studio(entry):
        if 'involved_companies' not in entry:
            return

        for company in entry['involved_companies']:
            if company['developer']:
                return company['company']['name']

    def get_content_rating(entry):

        esrb_rating_mapping = {
            6: 'RP',
            7: 'EC',
            8: 'E',
            9: 'E10',
            10: 'T',
            11: 'M',
        }

        pegi_rating_mapping = {
            1: '3',
            2: '7',
            3: '12',
            4: '16',
            5: '18',
        }

        if 'age_ratings' not in entry:
            return

        for company in entry['age_ratings']:

            # if company.get('category') == 1:
            #     return [esrb_rating_mapping.get(company.get('rating'))]

            if company.get('category') == 2:
                return [pegi_rating_mapping.get(company.get('rating'))]

    for media in medias:
        mapping = {
            'name': media.get('name'),
            'release_date': dateutil.parser.parse(f"{media.get('release_dates')[0].get('y')}-01-01").date() if
            media.get(
                'release_dates')[0].get('y') else None,
            'overview': media.get('summary'),
            'poster_path': 'https:' + media.get('cover').get('url').replace('t_thumb', 't_1080p') if media.get(
                'cover') else None,
            'media_type': media_type,
            'user_rating': None,
            'public_rating': media.get('total_rating') / 10 if media.get('total_rating') else None,
            'external_id': media.get('id'),
            'external_link': media.get('url'),
            'studio': get_studio(media),
            'content_ratings': map_associations(ContentRating, get_content_rating(media), media_type),
            'genres': map_associations(Genre, get_genres(media), media_type),
            'themes': map_associations(Theme, get_themes(media), media_type),
        }

        mapped_medias.append(Media(**mapping))

    return mapped_medias


def map_from_youtube(medias, media_type):
    def convert_text_to_date(text):

        if text is None:
            return None

        text = text.lower()

        if 'streamed' in text:
            text = text.replace('streamed', '')

        date = datetime.datetime.now().date()
        day = date.day
        month = date.month
        year = date.year

        if 'hour' in text:
            return f'{year}-{month}-{day}'

        if 'day' in text:
            number = text.split('day')[0]
            return f'{year}-{month}-{day - int(number)}'

        if 'month' in text:
            number = text.split('month')[0]
            return f'{year}-{month - int(number)}-{day}'

        if 'year' in text:
            number = text.split('year')[0]
            return f'{year - int(number)}-{month}-{day}'

    def convert_text_to_runtime(text):

        total_time_min = 0.0

        for elem in text.split(','):

            if 'hour' in elem:
                number = elem.split('hour')[0]
                total_time_min += 60 * int(number)

            if 'minute' in elem:
                number = elem.split('minute')[0]
                total_time_min += int(number)

            if 'second' in elem:
                number = elem.split('second')[0]
                total_time_min += int(number) / 60

        return int(total_time_min)

    mapped_medias = []

    for media in medias:
        mapping = {
            'name': media.get('title'),
            'release_date': dateutil.parser.parse(
                convert_text_to_date(media.get('publishedTime'))).date() if convert_text_to_date(
                media.get('publishedTime')) else None,
            'overview': media.get('summary'),
            'poster_path': f'https://img.youtube.com/vi/{media.get("id")}/maxresdefault.jpg',
            'media_type': media_type,
            'user_rating': None,
            'public_rating': media.get('public_rating') if media.get('public_rating') else None,
            'external_id': media.get('id'),
            'external_link': media.get('link'),
            'author': media.get('channel').get('name'),
            'runtime': convert_text_to_runtime(media.get('accessibility').get('duration')),
        }

        mapped_medias.append(Media(**mapping))

    return mapped_medias
