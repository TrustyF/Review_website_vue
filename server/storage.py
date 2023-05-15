import os
from tinydb import TinyDB, Query, where, operations
import re
from flask import Response

import functions


class StorageManager:
    def __init__(self):
        self.stores = {}
        self.curr_media = 'movie'

    def add_store(self, name, media):
        self.stores[name] = media

    def set_current_media(self, media_type):
        print('set current', media_type)
        self.curr_media = media_type

    def get_curr_media(self):
        print('returning', self.curr_media, self.stores[self.curr_media])
        return self.stores[self.curr_media]


class Media:

    def __init__(self, media_type):

        self.media_type = media_type

        self.base_path = os.path.dirname(__file__)
        self.db_path = os.path.join(self.base_path, f'database/{self.media_type}_db.json')

        self.db = TinyDB(self.db_path)

        self.filters = {}
        self.max_page_items = 50

        self.settings = {'session_seed': 0, }
        self.rank_range = (1, 10)

    # setters
    def set_settings(self, query):
        print('set_settings', query)
        self.settings = query
        self.max_page_items = 50

    def set_filters(self, query):
        print('set_filters', query)
        self.filters = query

    # post requests
    def load_more(self):
        self.max_page_items += 50

        if self.max_page_items >= len(self.db.all()):
            return Response(status=201)
        else:
            return Response(status=200)

    # getters

    def get_all_media(self):
        filtered_arr = self.filter(self.db)
        sorted_arr = self.sorting(filtered_arr)
        culled_arr = self.culling(sorted_arr)
        ranked_arr = functions.place_in_rank_category(culled_arr, self.rank_range)
        return ranked_arr

    # helpers
    def filter(self, f_arr):

        if self.filters == {}:
            return f_arr.all()

        rating_filters = self.filters['rating']['filter']
        length_filters = self.filters['length']['filter']
        genre_filters = self.filters['genre']['filter']
        region_filters = self.filters['region']['filter']
        format_filters = self.filters['format']['filter']
        searchbar_filters = self.filters['search_bar']

        format_query = region_query = genre_query = rating_query = length_query = searchbar_query = \
            Query().title.matches('[aZ]*')

        # filter format
        for format_filter in format_filters:
            match format_filter:
                case "Live-action":
                    format_query = (~Query().genres.any("Animation"))

                case "Animated":
                    format_query = (Query().genres.any("Animation"))

        # filter region
        for region_filter in region_filters:
            match region_filter:
                case "western":
                    region_query = (~Query().region.any("asian"))

                case "asian":
                    region_query = (Query().region.any("western"))

        # filter genre
        if len(genre_filters) > 0:
            genre_query = (Query().genres.all(genre_filters))

        #  filter rating
        if len(rating_filters) > 0:
            rating_query = (Query().my_rating.any(rating_filters))

        # filter length
        for length_filter in length_filters:
            match length_filter:
                case "0":
                    length_query = (Query().runtime <= 60)
                case "1":
                    length_query = (Query().runtime <= 120)
                case "2":
                    length_query = (120 < Query().runtime < 180)
                case "3":
                    length_query = (Query().runtime >= 180)

        # filter searchbar
        if len(searchbar_filters) > 0:
            searchbar_query = (Query().title.test(lambda val: re.search(searchbar_filters, val, re.IGNORECASE)))

        # return if empty
        # if len(queries) < 1:
        #     return f_arr.all()

        #  apply queries
        return f_arr.search(
            format_query &
            region_query &
            genre_query &
            rating_query &
            length_query &
            searchbar_query
        )

    def sorting(self, f_arr):
        # sort_arr = functions.sort_by_avg_rating(f_arr)
        # sort_arr = functions.sort_by_date_rated(f_arr)
        sort_arr = functions.sort_randomize(f_arr, self.settings['session_seed'])
        sort_arr = functions.sort_by_my_rating(sort_arr)
        return sort_arr

    def culling(self, f_arr):
        return f_arr[:self.max_page_items]

    # others
    def transfer_old(self):
        old_db = TinyDB(os.path.join(self.base_path, f'database/sorted_db.json'))
        self.db.insert_multiple(old_db.table('movies').search(where('media_type') == self.media_type))

    def test_media(self):
        print(self.media_type)
        print(self.db_path)


class Movies(Media):
    def __init__(self):
        super().__init__(media_type='movie')

    # others
    def cleanup(self):
        for mov in self.db.all():

            if 'images' not in mov:
                return
            if 'posters' not in mov['images']:
                return

            mov['posters'] = []

            for file in mov['images']['posters']:
                mov['posters'].append(file['file_path'])

            del mov['images']
            # print(mov['title'])

            try:
                self.db.table('_default').remove(Query().title == str(mov['title']))
                self.db.table('_default').insert(mov)
            except:
                print('keyError', mov['title'])


class Series(Media):
    def __init__(self):
        super().__init__(media_type='tv')

    def cleanup(self):
        for mov in self.db.all():
            print(mov['title'])

            if 'images' not in mov:
                return
            if 'posters' not in mov['images']:
                return

            mov['posters'] = []

            for file in mov['images']['posters']:
                mov['posters'].append(file['file_path'])

            del mov['images']
            del mov['credits']
            del mov['backdrop_path']
            del mov['created_by']
            del mov['episode_run_time']
            del mov['first_air_date']
            del mov['homepage']
            del mov['languages']
            del mov['last_air_date']
            del mov['last_episode_to_air']
            del mov['next_episode_to_air']
            del mov['networks']
            del mov['origin_country']
            del mov['production_companies']
            del mov['production_countries']
            del mov['spoken_languages']
            del mov['status']
            del mov['tagline']
            del mov['type']

            try:
                self.db.table('_default').remove(Query().title == str(mov['title']))
                self.db.table('_default').insert(mov)
            except:
                print('keyError', mov['title'])


# def edit_movie(query):
#     # print('query', query)
#     old_data = query['oldData']
#     new_data = query['newData']
#
#     title_query = Query().id == int(old_data['id'])
#     sorted_database.table(query['extra_settings']['media_type']).update(new_data, title_query)
#
#
# def add_movie(data):
#     print('adding movie', data)
#     if check_dupe(data):
#         print('adding ', data['title'])
#         sorted_database.table(data['media_type']).insert(data)
#     else:
#         print('movie already found! not added')
#
#
# def del_movie(data):
#     sorted_database.table(data['extra_settings']['media_type']).remove(Query().id == int(data['id']))
#
#
# def get_all_presets():
#     presets = (sorted_database.table('tag_presets').all())
#     sorted_presets = sorted(presets, key=lambda d: d['tier'])
#     return sorted_presets
#
#
# def add_preset(data):
#     sorted_database.table('tag_presets').insert(data)
#
#
# def del_preset(data):
#     sorted_database.table('tag_presets').remove(Query().name == str(data['name']))
#
#
# def check_dupe(data):
#     print('checking dupe ', data['title'])
#     title_query = Query().title.matches(str(data['title']))
#     entries = sorted_database.table(data['media_type']).search(title_query)
#
#     if len(entries) > 0:
#         state = True
#     else:
#         state = False
#
#     return state
store = StorageManager()
store.add_store('movie', Movies())
store.add_store('tv', Series())
