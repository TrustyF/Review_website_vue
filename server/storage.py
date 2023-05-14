import os
from tinydb import TinyDB, Query, where, operations
import re

import functions


class Media:

    def __init__(self, media_type):

        self.media_type = media_type

        self.base_path = os.path.dirname(__file__)
        self.db_path = os.path.join(self.base_path, f'database/{media_type}_db.json')

        self.db = TinyDB(self.db_path)

        self.filters = {}
        self.settings = {}
        self.rank_range = (1, 10)

    # setters
    def set_settings(self, query):
        print(query)
        self.filters = query
        self.settings = query['extra_settings']

    # getters
    def get_all_media(self):
        filtered_arr = self.filter(self.db)
        sorted_arr = self.sort(filtered_arr)
        culled_arr = self.cull(sorted_arr)
        ranked_arr = functions.place_in_rank_category(culled_arr, self.rank_range)
        return ranked_arr

    # helpers
    def filter(self, f_arr):
        rating_filters = self.filters['rating']['filter']
        length_filters = self.filters['length']['filter']
        genre_filters = self.filters['genre']['filter']
        region_filters = self.filters['region']['filter']
        format_filters = self.filters['format']['filter']
        type_filters = self.filters['type']['filter']
        searchbar_filters = self.filters['search_bar']

        queries = []

        # filter type
        for type_filter in type_filters:
            match type_filter:
                case "Movie":
                    queries.append(Query().media_type == "movie")

                case "Tv-series":
                    queries.append(Query().media_type == "tv")

                case "Documentary":
                    queries.append(Query().genres.any("Documentary"))

        # filter format
        for format_filter in format_filters:
            match format_filter:
                case "Live-action":
                    queries.append(~Query().genres.any("Animation"))

                case "Animated":
                    queries.append(Query().genres.any("Animation"))

        # filter region
        for region_filter in region_filters:
            match region_filter:
                case "western":
                    queries.append(~Query().region.any("asian"))

                case "asian":
                    queries.append(Query().region.any("western"))

        # filter genre
        if len(genre_filters) > 0:
            queries.append(Query().genres.all(genre_filters))

        #  filter rating
        if len(rating_filters) > 0:
            queries.append(Query().my_rating.any(rating_filters))

        # filter length
        for length_filter in length_filters:
            # ignore tv
            queries.append(Query().media_type != "tv")

            match length_filter:
                case "0":
                    queries.append(Query().runtime <= 60)
                case "1":
                    queries.append(Query().runtime <= 120)
                case "2":
                    queries.append(120 < Query().runtime < 180)
                case "3":
                    queries.append(Query().runtime >= 180)

        # filter searchbar
        if len(searchbar_filters) > 0:
            queries.append(Query().title.test(lambda val: re.search(searchbar_filters, val, re.IGNORECASE)))

        # return if empty
        if len(queries) < 1:
            return f_arr.all()

        #  apply queries
        return f_arr.search(queries)

    def sort(self, f_arr):
        # sort_arr = functions.sort_by_avg_rating(f_arr)
        # sort_arr = functions.sort_by_date_rated(f_arr)
        # sort_arr = functions.sort_randomize(f_arr, self.settings['session_seed'])
        # sort_arr = functions.sort_by_my_rating(sort_arr)
        return f_arr

    def cull(self, f_arr):
        return f_arr

    # others
    def transfer_old(self):
        old_db = TinyDB(os.path.join(self.base_path, f'database/sorted_db.json'))

        if self.media_type == 'movie':
            self.db.insert_multiple(old_db.table('movies').search(where('media_type') == 'movie'))

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

movie_store = Media('movie')
