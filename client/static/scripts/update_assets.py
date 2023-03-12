import json
import os
# from os.path import *
# from os import *
import pprint as pp
from collections import defaultdict
from functools import reduce
from pathlib import Path
from itertools import zip_longest

dir_path = "D://A_Mod//A_Projects//Web design//movie_site_vue//public//assets//tags"
target = "D://A_Mod//A_Projects//Web design//movie_site_vue//public//assets//tags//assets.json"

ignore_files = ['assets.json', 'update_assets.py']


def build_dict(path, key=None):
    directory_dict = {}
    directory_list = []

    for item in os.listdir(path):
        if item in ignore_files:
            continue

        print(item)

        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directory_dict[item] = build_dict(item_path, item)

        else:
            directory_list.append(item)
            if len(directory_list) == len(os.listdir(path)):
                return directory_list

    return directory_dict


export = build_dict(dir_path)

with open(target, "w") as outfile:
    json.dump(export, outfile, indent=2)
