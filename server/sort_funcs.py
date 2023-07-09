from datetime import datetime
import random
import re


def sort_by_my_rating(f_arr):
    # return sorted(f_arr, key=lambda k: k['my_rating'], reverse=True)
    f_arr.sort(key=lambda x: '{0:0>8}'.format(x['my_rating']).lower(), reverse=True)
    return f_arr


def sort_by_avg_rating(f_arr):
    return sorted(f_arr, key=lambda k: k['vote_average'], reverse=True)


def sort_by_date_rated(f_arr):
    return sorted(f_arr, key=lambda k: datetime.strptime(k['date_rated'].split(" ")[0], '%Y-%m-%d'), reverse=True)


def sort_by_date_released(f_arr):
    return sorted(f_arr, key=lambda k: datetime.strptime(k['release_date'], '%Y-%m-%d'), reverse=True)


def sort_randomize(f_arr, f_seed=0):
    if f_seed == 0:
        random.shuffle(f_arr)
        return f_arr
    else:
        random.Random(f_seed).shuffle(f_arr)
        return f_arr


# rank
def place_in_rank_category(f_arr, f_rank_range):
    # print('rank ranges',f_rank_range)
    ranked = {}

    for rank in range(f_rank_range[0], f_rank_range[1]):
        ranked[rank] = [mov for mov in f_arr if mov['my_rating'] == str(rank)]

    return ranked
