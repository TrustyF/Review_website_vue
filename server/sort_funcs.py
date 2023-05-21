from datetime import datetime
import random


def sort_by_my_rating(f_arr):
    return sorted(f_arr, key=lambda k: k['my_rating'], reverse=True)


def sort_by_avg_rating(f_arr):
    return sorted(f_arr, key=lambda k: k['vote_average'], reverse=True)


def sort_by_date_rated(f_arr):
    return sorted(f_arr, key=lambda k: datetime.strptime(k['date_rated'], '%Y-%m-%d'), reverse=True)


def sort_randomize(f_arr, f_seed):
    random.Random(f_seed).shuffle(f_arr)
    return f_arr


# rank
def place_in_rank_category(f_arr, f_rank_range):
    ranked = {}

    for rank in range(f_rank_range[0], f_rank_range[1]):
        ranked[rank] = [mov for mov in f_arr if mov['my_rating'] == str(rank)]

    return ranked
