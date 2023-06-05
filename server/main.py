import random

from flask import Flask, Request, request, Response
from flask_cors import CORS
# from flask_caching import Cache

from storage import store, tag_presets

app = Flask(__name__)
# app.config['CACHE_TYPE'] = "FileSystemCache"
# app.config['CACHE_DIR'] = "cache"
CORS(app)

# cache = Cache(app)
media_store = store.stores


#  Media
@app.route('/media/get_all', methods=["POST"])
def get_all():
    # print('get all')
    return media_store[request.json['media_type']].get_all_media(request.json), 200


@app.route('/media/add', methods=["POST"])
def add():
    media_store[request.json['media_type']].add_media(request.json)
    return 200


@app.route('/media/update', methods=["PUT"])
def update():
    media_store[request.json['media_type']].update_media(request.json)
    return 200


@app.route('/media/delete', methods=["DELETE"])
def delete():
    media_store[request.json['media_type']].del_media(request.json)
    return 200


# Get covers
@app.route('/media/cover', methods=["GET"])
# @cache.cached(timeout=3000)
def get_cover():
    poster_path = request.args.get('poster_path')
    media_type = request.args.get('type')
    return media_store[media_type].get_cover(poster_path)


# Extras
@app.route('/media/get_rating_ranges', methods=["GET"])
# @cache.cached(timeout=3000)
def get_rating_range():
    # print(request.args.get('test'), request.args.get('good'))
    return store.gather_rating_ranges()


@app.route('/media/check_dupe', methods=["POST"])
def check_dupe():
    print('check_dupe')
    return media_store[request.json['media_type']].check_dupe(request.json), 200


# Selective picks
@app.route('/media/get_rand_genre', methods=["POST"])
def get_rand_genre():
    return media_store[request.json['media_type']].get_rand_genre(request.json), 200


@app.route('/media/get_recent_release', methods=["POST"])
# @cache.cached(timeout=3000)
def get_recent_release():
    return media_store[request.json['media_type']].get_recent_release(request.json), 200


# class Tags:
#     def __init__(self):
#         self.presets = tag_presets
#
#     def get(self):
#         return self.presets.get_all_presets(), 200
#
#     def post(self):
#         req = request.json
#         return self.presets.add_preset(req), 200
#
#     def delete(self):
#         req = request.json
#         return self.presets.del_preset(req), 200

if __name__ == '__main__':
    app.run(debug=True)
