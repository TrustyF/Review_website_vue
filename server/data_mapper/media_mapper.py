import datetime
import math

import dateutil.parser
from dateutil.relativedelta import relativedelta

import json
from pprint import pprint
import time

from db_loader import db
from sql_models.media_model import Media, Genre, Theme, ContentRating
from sqlalchemy import func
from flask import jsonify


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


def map_from_tmdb(medias, media_type):
    def get_movie_content_rating_conversion_table(pg_rating):
        table = {
            'G': ['U'],
            'PG': ['TP', '7'],
            'PG-13': ['-12', '12', '+12', '12+', 'PG13'],
            'R': ['-16', '16', '15', '+15', '15+', 'PG15'],
            'NC-17': ['-18', '18', '+18', '18+', 'R18'],
        }
        return table[pg_rating]

    def get_tv_content_rating_conversion_table(pg_rating):
        table = {
            'TV-Y': [],
            'TV-Y7': [],
            'TV-G': ['TP', '7'],
            'TV-PG': ['-12', '12', '+12', '12+', 'PG13'],
            'TV-14': ['-16', '15', '+15', '15+', 'PG15'],
            'TV-MA': ['-18', '18', '+18', '18+', 'R18'],
        }
        return table[pg_rating]

    def mapping_tmdb_movie(entry):

        def get_content_rating():
            db_content_ratings = [x.name for x in db.session.query(ContentRating).join(Media.content_rating).filter(
                Media.media_type == media_type).all()]

            content_rating = ''
            if 'releases' in entry:
                grouped = [[y['iso_3166_1'], y['certification']] for y in entry['releases']['countries']]
                # print(grouped)

                all_ratings = [x[1] for x in grouped if x[1] != '']
                us_grouped = [x for x in grouped if x[0] == 'US' if x[1] != '' and x[1] != 'NR']

                if us_grouped:
                    for i in us_grouped:
                        if i[1]:
                            # print('us content')
                            content_rating = i[1]
                            break

                else:
                    for rating in db_content_ratings:
                        equivalent = get_movie_content_rating_conversion_table(rating)

                        if rating in all_ratings:
                            # print('other content')
                            content_rating = rating
                            break

                        else:
                            for eq in equivalent:
                                if eq in all_ratings:
                                    # print('equivalent content', rating, eq)
                                    content_rating = rating
                                    break
                            else:
                                continue
                            break

            return content_rating

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
            'external_name': entry.get('title'),
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
            'content_rating': db.session.query(ContentRating).filter_by(name=get_content_rating()).one_or_none(),
            'genres': map_associations(Genre, get_genres(), media_type),
        }

        return movie_mapping

    def mapping_tmdb_tv(entry):

        def get_content_rating():

            db_content_ratings = [x.name for x in db.session.query(ContentRating).join(Media.content_rating).filter(
                Media.media_type == media_type).all()]

            content_rating = ''
            if 'content_ratings' in entry:
                grouped = [[y['iso_3166_1'], y['rating']] for y in entry['content_ratings']['results']]
                # print(grouped)

                all_ratings = [x[1] for x in grouped if x[1] != '']
                us_grouped = [x for x in grouped if x[0] == 'US' if x[1] != '']

                if us_grouped:
                    for i in us_grouped:
                        if i[1]:
                            # print('us content')
                            content_rating = i[1]
                            break

                else:
                    for rating in db_content_ratings:
                        equivalent = get_tv_content_rating_conversion_table(rating)

                        if rating in all_ratings:
                            # print('other content')
                            content_rating = rating
                            break

                        else:
                            for eq in equivalent:
                                if eq in all_ratings:
                                    # print('equivalent content', rating, eq)
                                    content_rating = rating
                                    break
                            else:
                                continue
                            break

            return content_rating

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
            'external_name': entry.get('name'),
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
            'content_rating': db.session.query(ContentRating).filter_by(name=get_content_rating()).one_or_none(),
            'genres': map_associations(Genre, get_genres(), media_type),
        }
        return tv_mapping

    mapped_medias = []
    for media in medias:

        mapping = {}

        if media_type in ['movie']:
            mapping = mapping_tmdb_movie(media)
        if media_type in ['tv']:
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
            'external_name': attrib.get('title').get('en'),
            'release_date': dateutil.parser.parse(f"{attrib.get('year')}-01-01").date() if attrib.get('year') else None,
            'overview': attrib.get('description').get('en'),
            'poster_path': media.get('poster_path'),
            'media_type': media_type,
            'user_rating': None,
            'public_rating': media.get('vote_average'),
            'external_id': media.get('id'),
            'external_link': 'https://mangadex.org/title/' + media.get('id'),
            'author': get_author(media),
            'content_rating': db.session.query(ContentRating).filter_by(name=attrib.get('contentRating')).one_or_none(),
            'genres': map_associations(Genre, get_genres(media), media_type),
        }

        mapped_medias.append(Media(**mapping))

    return mapped_medias


def map_from_comic_vine(medias, media_type):
    mapped_medias = []

    for media in medias:
        mapping = {
            'name': media.get('name'),
            'external_name': media.get('name'),
            'release_date': dateutil.parser.parse(f"{media.get('start_year')}-01-01").date(),
            'overview': media.get('description'),
            'poster_path': media.get('image').get('medium_url'),
            'media_type': media_type,
            'user_rating': None,
            'public_rating': 0,
            'external_id': media.get('id'),
            'external_link': media.get('site_detail_url'),
            'author': media.get('publisher').get('name'),
            # 'content_rating': db.session.query(ContentRating),
            # 'genres': map_associations(Genre, get_genres(media), media_type),
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
            #     return esrb_rating_mapping.get(company.get('rating'))

            if company.get('category') == 2:
                return pegi_rating_mapping.get(company.get('rating'))

    for media in medias:
        mapping = {
            'name': media.get('name'),
            'external_name': media.get('name'),
            'release_date': dateutil.parser.parse(f"{media.get('release_dates')[0].get('y')}-01-01").date() if
            media.get('release_dates') and len(media.get('release_dates')) > 0 and media.get('release_dates')[0].get(
                'y') else None,
            'overview': media.get('summary'),
            'poster_path': 'https:' + media.get('cover').get('url').replace('t_thumb', 't_1080p') if media.get(
                'cover') else None,
            'media_type': media_type,
            'user_rating': None,
            'public_rating': media.get('total_rating') / 10 if media.get('total_rating') else None,
            'external_id': media.get('id'),
            'external_link': media.get('url'),
            'studio': get_studio(media),
            'content_rating': db.session.query(ContentRating).filter_by(name=get_content_rating(media)).one_or_none(),
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
            number = int(text.split('day')[0])
            return (datetime.date.today() - relativedelta(days=number)).strftime('%Y-%m-%d')

        if 'week' in text:
            number = int(text.split('week')[0])
            return (datetime.date.today() - relativedelta(weeks=number)).strftime('%Y-%m-%d')

        if 'month' in text:
            number = int(text.split('month')[0])
            return (datetime.date.today() - relativedelta(months=number)).strftime('%Y-%m-%d')

        if 'year' in text:
            number = int(text.split('year')[0])
            return (datetime.date.today() - relativedelta(years=number)).strftime('%Y-%m-%d')

    def convert_text_to_runtime(text):

        # print(text)

        if text is None:
            return

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

        return int(math.ceil(total_time_min))

    mapped_medias = []

    for media in medias:
        mapping = {
            'name': media.get('title'),
            'external_name': media.get('title'),
            'release_date': dateutil.parser.parse(
                convert_text_to_date(media.get('publishedTime'))).date() if convert_text_to_date(
                media.get('publishedTime')) else None,
            'overview': media.get('summary'),
            'poster_path': f'https://img.youtube.com/vi/{media.get("id")}/maxresdefault.jpg',
            'media_type': media_type,
            'user_rating': None,
            'public_rating': media.get('public_rating') if media.get('public_rating') else None,
            'external_id': media.get('id'),
            'video_link': media.get('link'),
            'author': media.get('channel').get('name'),
            'runtime': convert_text_to_runtime(media.get('accessibility').get('duration')),
        }

        mapped_medias.append(Media(**mapping))

    return mapped_medias
