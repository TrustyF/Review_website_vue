import datetime
import json
import os
import pprint
import time

from tinydb import TinyDB, Query, where, operations
import re
from flask import Response, Request
import requests

import sort_funcs
import filter_funcs
from constants import TMDB_API_KEY, TMDB_ACCESS_TOKEN


class Presets:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)
        self.db_path = os.path.join(self.base_path, f'database/presets_db.json')

        self.db = TinyDB(self.db_path)

    def get_all_presets(self):
        return sorted(self.db.all(), key=lambda d: d['tier'])

    def add_preset(self, data):
        self.db.insert(data)

    def del_preset(self, data):
        self.db.remove(Query().name == str(data['name']))


class StorageManager:
    def __init__(self):
        self.stores = {}
        self.curr_media = 'movie'

    def add_store(self, name, media):
        self.stores[name] = media

    def gather_rating_ranges(self):
        out = {}
        for media in self.stores:
            out[self.stores[media].media_type] = self.stores[media].get_media_rating_range()
        return out


# noinspection PyMethodMayBeStatic
class Media:

    def __init__(self, media_type):

        self.media_type = media_type

        self.base_path = os.path.dirname(__file__)
        self.db_path = os.path.join(self.base_path, f'database/{self.media_type}_db.json')

        self.db = TinyDB(self.db_path)
        self.list_db = self.db.all()

        self.rank_range = (1, 10)

    # setters
    def set_settings(self, f_settings=None, f_max_media=10):
        # print('set_settings')
        self.settings = f_settings
        self.max_page_items = f_max_media

    def set_filters(self, query):
        # print('set_filters')
        self.filters = query

    # operations
    def add_media(self, data):
        self.db.insert(data['data'])

    # noinspection PyTypeChecker
    def update_media(self, data):
        # print('update test ', data)
        query = Query().id == data['data']['id']
        test = self.db.update(data['data'], query)
        # print('update test result', test)

    def del_media(self, data):
        query = Query().id == str(data['id'])
        self.db.remove(query)

    def check_dupe(self, media_id):
        query = Query().id == str(media_id)
        entries = self.db.search(query)
        if len(entries) > 0:
            return {'result': True}
        else:
            return {'result': False}

    # search
    def search_media(self, f_title, f_page, f_id):
        title = f_title
        page = f_page

        if f_id is None:

            page = int(f_page)

            # phase 1
            request = f'https://api.themoviedb.org/3/search/{self.media_type}?api_key={TMDB_API_KEY}' \
                      f'&language=en-US&query={title}'
            response = requests.get(request).json()

            if len(response['results']) < 1:
                return

            simple_data = response['results'][page]
        else:

            # phase 1
            request = f'https://api.themoviedb.org/3/find/{f_id}?external_source=imdb_id'
            headers = {
                "accept": "application/json",
                "Authorization": 'Bearer ' + TMDB_ACCESS_TOKEN
            }

            response = requests.get(request, headers=headers).json()

            simple_data = response[f'{self.media_type}_results'][0]

            if len(response['movie_results']) > 1:
                raise Exception('more than one result found for ', title)

                # phase 2
        extra_request = f'https://api.themoviedb.org/3/{self.media_type}/{simple_data["id"]}?api_key={TMDB_API_KEY}' \
                        f'&language=en-US&append_to_response=credits,images&include_image_language=en,null'
        full_data = requests.get(extra_request).json()

        # format data
        formatted_data = {
            'title': simple_data['title'],
            'date_rated': str(datetime.date.today()),
            'genres': [x['name'] for x in full_data['genres']],
            'id': simple_data['id'],
            'media_type': self.media_type,
            'my_rating': None,
            'overview': simple_data['overview'],
            'poster_path': simple_data['poster_path'],
            'release_date': simple_data['release_date'],
            'tags': None,
            'vote_average': simple_data['vote_average'],

            'runtime': full_data['runtime'],
            'imdb_id': full_data['imdb_id'],
        }

        return formatted_data

    def search_extra_posters(self, f_id):

        request = f'https://api.themoviedb.org/3/find/{f_id}?external_source=imdb_id'
        headers = {
            "accept": "application/json",
            "Authorization": 'Bearer ' + TMDB_ACCESS_TOKEN
        }

        response = requests.get(request, headers=headers).json()
        simple_data = response[f'{self.media_type}_results'][0]

        extra_request = f'https://api.themoviedb.org/3/{self.media_type}/{simple_data["id"]}?api_key={TMDB_API_KEY}' \
                        f'&language=en-US&append_to_response=credits,images&include_image_language=en,null'
        full_data = requests.get(extra_request).json()

        posters = [x['file_path'] for x in full_data['images']['posters']]

        return posters

    # others
    def refresh(self):
        print('refresh', self.media_type)
        mov_list = self.db.all()
        for index, entry in enumerate(mov_list):

            new_data = self.search_media(entry['title'], None, entry['imdb_id'])
            if 'my_rating' in entry:
                new_data['my_rating'] = entry['my_rating']
            if 'tags' in entry:
                new_data['tags'] = entry['tags']
            if 'date_rated' in entry:
                new_data['date_rated'] = entry['date_rated']

            # disabled for safety
            self.db.remove(Query().imdb_id == str(entry['imdb_id']))
            self.db.insert(new_data)

    # post requests
    def load_more(self):
        self.max_page_items += 50

        if self.max_page_items >= len(self.db.all()):
            return Response(status=201)
        else:
            return Response(status=200)

    # getters
    def get_all_media(self, data):
        self.set_settings(data['settings'], data['max_media'])
        self.set_filters(data['filters'])
        filtered_arr = self.filter(self.db)
        sorted_arr = self.sorting(filtered_arr)
        culled_arr = self.culling(sorted_arr, self.max_page_items)
        ranked_arr = sort_funcs.place_in_rank_category(culled_arr, self.rank_range)
        return ranked_arr

    def get_media_rating_range(self):
        avg_ratings = []
        my_ratings = []

        for mov in self.db:
            try:
                avg_ratings.append(float(mov['vote_average']))
                my_ratings.append(float(mov['my_rating']))
            except KeyError as e:
                print(mov, 'has no avg rating', e)

        tuple_avg = (min(avg_ratings), max(avg_ratings))
        tuple_rating = (min(my_ratings), max(my_ratings))

        return {
            'avg_range': tuple_avg,
            'my_range': tuple_rating
        }

    def get_media_genres(self):
        pass

    # selective pickers
    def get_rand_genre(self, data):
        # print(data['max_media'])
        filtered_arr = self.db.search(filter_funcs.rating_filter({'rating': {'filter': ['6', '7', '8', '9']}}))
        sort_arr = sort_funcs.sort_randomize(filtered_arr, data['session_seed'])
        picked_arr = filter_funcs.pick_one_each_genre(sort_arr)
        culled_arr = self.culling(picked_arr, data['max_media'])
        # ranked_arr = sort_funcs.place_in_rank_category(filtered_arr, self.rank_range)
        return culled_arr

    def get_recent_release(self, data):
        sort_arr = sort_funcs.sort_by_date_released(self.db)
        culled_arr = self.culling(sort_arr, data['max_media'])
        return culled_arr

    # helpers
    def filter(self, f_arr):
        return f_arr.search(
            filter_funcs.rating_filter(self.filters) &
            filter_funcs.length_filter(self.filters) &
            filter_funcs.genre_filter(self.filters) &
            filter_funcs.region_filter(self.filters) &
            filter_funcs.format_filter(self.filters) &
            filter_funcs.searchbar_filter(self.filters)
        )

    def sorting(self, f_arr):
        match self.filters['sort']['filter'][0]:
            case 'popular_vote':
                sort_arr = sort_funcs.sort_by_avg_rating(f_arr)
            case 'date_rated':
                sort_arr = sort_funcs.sort_by_date_rated(f_arr)
            case 'release_date':
                sort_arr = sort_funcs.sort_by_date_released(f_arr)
            case _:
                sort_arr = sort_funcs.sort_randomize(f_arr, self.settings['session_seed'])

        sort_arr = sort_funcs.sort_by_my_rating(sort_arr)
        return sort_arr

    def culling(self, f_arr, max_items):
        return f_arr[:max_items]

    # others
    def transfer_old(self):
        old_db = TinyDB(os.path.join(self.base_path, f'database/sorted_db.json'))
        self.db.insert_multiple(old_db.table('movies').search(where('media_type') == self.media_type))


class Movies(Media):
    def __init__(self):
        super().__init__(media_type='movie')


class Series(Media):
    def __init__(self):
        super().__init__(media_type='tv')

    def search_media(self, f_title, f_page, f_id):
        title = f_title
        page = f_page

        if f_id is None:

            page = int(f_page)

            # phase 1
            request = f'https://api.themoviedb.org/3/search/{self.media_type}?api_key={TMDB_API_KEY}' \
                      f'&language=en-US&query={title}'
            response = requests.get(request).json()

            simple_data = response['results'][page]
        else:

            # phase 1
            request = f'https://api.themoviedb.org/3/find/{f_id}?external_source=imdb_id'
            headers = {
                "accept": "application/json",
                "Authorization": 'Bearer ' + TMDB_ACCESS_TOKEN
            }

            response = requests.get(request, headers=headers).json()

            simple_data = response[f'{self.media_type}_results'][0]

            if len(response['movie_results']) > 1:
                raise Exception('more than one result found for ', title)

                # phase 2
        extra_request = f'https://api.themoviedb.org/3/{self.media_type}/{simple_data["id"]}?api_key={TMDB_API_KEY}' \
                        f'&language=en-US&append_to_response=credits,images&include_image_language=en,null'
        full_data = requests.get(extra_request).json()
        # pprint.pprint(simple_data)

        # format data
        formatted_data = {
            'title': simple_data['name'],
            'date_rated': str(datetime.date.today()),
            'genres': [x['name'] for x in full_data['genres']],
            'id': simple_data['id'],
            'media_type': self.media_type,
            'my_rating': None,
            'overview': simple_data['overview'],
            'poster_path': simple_data['poster_path'],
            'release_date': simple_data['first_air_date'],
            'tags': None,
            'vote_average': simple_data['vote_average'],

            'episodes': full_data['number_of_episodes'],
            'seasons': full_data['number_of_seasons'],
            'imdb_id': f_id,
        }

        return formatted_data

    def refresh(self):
        print('refresh', self.media_type)

        mov_list = self.db.all()
        for index, entry in enumerate(mov_list):

            if "imdb_id" not in entry:
                entry['imdb_id'] = entry['imdb_url'].split('/')[4]

            new_data = self.search_media(entry['title'], None, entry['imdb_id'])
            if 'my_rating' in entry:
                new_data['my_rating'] = entry['my_rating']
            if 'tags' in entry:
                new_data['tags'] = entry['tags']
            if 'date_rated' in entry:
                new_data['date_rated'] = entry['date_rated']

            # disabled for safety
            self.db.remove(Query().imdb_id == str(entry['imdb_id']))
            self.db.insert(new_data)


class Manga(Media):
    def __init__(self):
        super().__init__(media_type='manga')

    # getters
    def search_media(self, f_title, f_page, f_id=None):
        title = f_title
        page = f_page

        if f_id is None:
            page = int(f_page)

        # phase 1
        if f_id is None:
            request = f'https://api.mangadex.org/manga?title={title}' \
                      f'&order%5Brelevance%5D=desc&includes[]=cover_art&limit=20'
        else:
            request = f'https://api.mangadex.org/manga/{f_id}?includes%5B%5D=cover_art'

        response = requests.get(request).json()

        if response['result'] != 'ok':
            return {'result': False}

        if len(response['data']) == 0:
            return {'result': False}

        if f_page is not None:
            if len(response['data']) < page:
                return {'result': False}

        if f_page is None:
            simple_data = response['data']['attributes']
            all_data = response['data']
        else:
            simple_data = response['data'][page]['attributes']
            all_data = response['data'][page]

        # phase 2

        formatted_data = {
            'title': None,
            'date_rated': str(datetime.date.today()),
            'genres': [x['attributes']['name']['en'] for x in simple_data['tags'] if
                       x['attributes']['group'] == 'genre'],
            'id': all_data['id'],
            'media_type': 'manga',
            'my_rating': None,
            'overview': None,
            'poster_path': None,
            'release_date': str(simple_data['year']) + '-01-01',
            'tags': None,
            'vote_average': None,

            'contentRating': simple_data['contentRating'],
        }

        # clean titles
        if 'en' in simple_data['title']:
            formatted_data['title'] = simple_data['title']['en']
        elif 'ja' in simple_data['title']:
            formatted_data['title'] = simple_data['title']['ja']

        # clean desc
        if 'en' in simple_data['description']:
            formatted_data['overview'] = simple_data['description']['en']
        else:
            formatted_data['overview'] = 'No description available'

        # phase 3

        request = f'https://api.mangadex.org/cover?limit=100&manga%5B%5D={formatted_data["id"]}'
        response = requests.get(request).json()

        #  fix volumes none
        for poster in response["data"]:
            if poster["attributes"]['volume'] is None:
                poster["attributes"]['volume'] = str(len(response["data"]))

        poster = sorted(response["data"], key=lambda x: x["attributes"]["volume"])
        formatted_data['poster_path'] = f'{formatted_data["id"]}/' \
                                        f'{poster[0]["attributes"]["fileName"]}'

        # phase 4

        request = f'https://api.mangadex.org/statistics/manga/{formatted_data["id"]}'
        response = requests.get(request).json()
        formatted_data['vote_average'] = response['statistics'][formatted_data["id"]]['rating']['average']

        return formatted_data

    def search_extra_posters(self, f_id):

        request = f'https://api.mangadex.org/cover?limit=100&manga%5B%5D={f_id}'
        response = requests.get(request).json()

        #  fix volumes none
        for poster in response["data"]:
            if poster["attributes"]['volume'] is None:
                poster["attributes"]['volume'] = str(len(response["data"]))

        # full_data = sorted(response["data"], key=lambda x: x["attributes"]["volume"])
        full_data = sorted(response["data"], key=lambda x: '{0:0>8}'.format(x["attributes"]["volume"]).lower())

        posters = []
        for image in full_data:
            posters.append(f"{f_id}/{image['attributes']['fileName']}")

        return posters

    # helpers

    def filter(self, f_arr):
        return f_arr.search(
            filter_funcs.rating_filter(self.filters) &
            filter_funcs.genre_filter(self.filters) &
            filter_funcs.content_filter(self.filters) &
            filter_funcs.searchbar_filter(self.filters)
        )

    # selective pickers
    def get_rand_genre(self, data):
        # print(data['max_media'])
        filtered_arr = self.db.search(
            filter_funcs.rating_filter({
                'rating': {'filter': ['7', '8', '9']},
            }) &
            filter_funcs.content_filter({
                'content': {
                    'filter': ["safe", "suggestive"],
                    'available': ["safe", "suggestive", "erotica", "pornographic"]
                }
            })
        )
        sort_arr = sort_funcs.sort_randomize(filtered_arr)
        picked_arr = filter_funcs.pick_one_each_genre(sort_arr)
        culled_arr = self.culling(picked_arr, data['max_media'])
        # ranked_arr = sort_funcs.place_in_rank_category(filtered_arr, self.rank_range)
        return culled_arr

    # getters
    def get_cover(self, poster_path):
        # print('get cover', poster_path)
        request = f'https://uploads.mangadex.org/covers/{poster_path}.256.jpg'
        return requests.get(request).content

    def refresh(self):
        print('refresh')
        for index, entry in enumerate(self.db.all()):

            # if index < 50:
            #     continue

            print(entry['title'])

            new_data = self.search_media(entry['title'], None, entry['id'])
            if 'my_rating' in entry:
                new_data['my_rating'] = entry['my_rating']
            if 'tags' in entry:
                new_data['tags'] = entry['tags']
            if 'contentRating' in entry:
                new_data['contentRating'] = entry['contentRating']
            if 'dropped' in entry:
                new_data['dropped'] = entry['dropped']

            # disabled for safety
            self.db.remove(Query().id == str(entry['id']))
            self.db.insert(new_data)


class Anime(Media):
    def __init__(self):
        super().__init__(media_type='anime')

    def search_media(self, f_title, f_page, f_id):
        title = f_title
        page = f_page

        if f_id is None:

            page = int(f_page)

            # phase 1
            request = f'https://api.themoviedb.org/3/search/{self.media_type}?api_key={TMDB_API_KEY}' \
                      f'&language=en-US&query={title}'
            response = requests.get(request).json()
            simple_data = response['results'][page]

        else:

            # phase 1
            request = f'https://api.themoviedb.org/3/find/{f_id}?external_source=imdb_id'
            headers = {
                "accept": "application/json",
                "Authorization": 'Bearer ' + TMDB_ACCESS_TOKEN
            }

            response = requests.get(request, headers=headers).json()
            simple_data = response['tv_results'][0]

            if len(response['movie_results']) > 1:
                raise Exception('more than one result found for ', title)

                # phase 2
        extra_request = f'https://api.themoviedb.org/3/tv/{simple_data["id"]}?api_key={TMDB_API_KEY}' \
                        f'&language=en-US&append_to_response=credits,images&include_image_language=en,null'
        full_data = requests.get(extra_request).json()
        # pprint.pprint(full_data)

        # format data
        formatted_data = {
            'title': simple_data['name'],
            'date_rated': str(datetime.date.today()),
            'genres': [x['name'] for x in full_data['genres']],
            'id': simple_data['id'],
            'media_type': self.media_type,
            'my_rating': None,
            'overview': simple_data['overview'],
            'poster_path': simple_data['poster_path'],
            'release_date': simple_data['first_air_date'],
            'tags': None,
            'vote_average': simple_data['vote_average'],

            'episodes': full_data['number_of_episodes'],
            'seasons': full_data['number_of_seasons'],
            'imdb_id': f_id,
        }

        return formatted_data

    def refresh(self):
        print('refresh', self.media_type)

        mov_list = self.db.all()
        for index, entry in enumerate(mov_list):

            print(entry['title'])

            if "imdb_id" not in entry:
                entry['imdb_id'] = entry['imdb_url'].split('/')[4]

            new_data = self.search_media(entry['title'], None, entry['imdb_id'])
            if 'my_rating' in entry:
                new_data['my_rating'] = entry['my_rating']
            if 'tags' in entry:
                new_data['tags'] = entry['tags']
            if 'date_rated' in entry:
                new_data['date_rated'] = entry['date_rated']

            # disabled for safety
            self.db.remove(Query().title == str(entry['title']))
            self.db.insert(new_data)


tag_presets = Presets()

store = StorageManager()
store.add_store('movie', Movies())
store.add_store('tv', Series())
store.add_store('manga', Manga())
store.add_store('anime', Anime())
