import pprint
import random

from flask import Flask, Request, request, Response
from flask_cors import CORS
# from flask_caching import Cache
import flask_color
import random

from storage import store, tag_presets

app = Flask(__name__)
app.config['DEBUG'] = True
flask_color.init_app(app)
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
    print('add media', request.json)
    media_store[request.json['media_type']].add_media(request.json)
    return 'OK'


@app.route('/media/update', methods=["POST"])
def update():
    media_store[request.json['media_type']].update_media(request.json)
    return 'OK'


@app.route('/media/delete', methods=["POST"])
def delete():
    media_store[request.json['media_type']].del_media(request.json)
    return 'OK'


@app.route('/media/search', methods=["GET"])
def search():
    title = request.args.get('title')
    page = request.args.get('page')
    media_type = request.args.get('type')
    return media_store[media_type].search_media(title, page)


@app.route('/media/extra_posters', methods=["GET"])
def extra_posters():
    media_id = request.args.get('media_id')
    media_type = request.args.get('media_type')
    return media_store[media_type].search_extra_posters(media_id)


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
    if random.randint(0,1) == 1:
        return store.gather_rating_ranges()
    else:
        print('failed rand check')
        return {}


@app.route('/media/check_dupe', methods=["GET"])
def check_dupe():
    media_id = request.args.get('media_id')
    media_type = request.args.get('media_type')
    return media_store[media_type].check_dupe(media_id)


# Selective picks
@app.route('/media/get_rand_genre', methods=["POST"])
def get_rand_genre():
    return media_store[request.json['media_type']].get_rand_genre(request.json), 200


@app.route('/media/get_recent_release', methods=["POST"])
# @cache.cached(timeout=3000)
def get_recent_release():
    return media_store[request.json['media_type']].get_recent_release(request.json), 200


# presets

@app.route('/preset/get_all', methods=["GET"])
def get_all_presets():
    return tag_presets.get_all_presets(), 200


@app.route('/preset/add', methods=["POST"])
def add_preset():
    return tag_presets.add_preset(request.json), 200


@app.route('/preset/delete', methods=["POST"])
def del_preset():
    return tag_presets.del_preset(request.json), 200


if __name__ == '__main__':
    # media_store['anime'].refresh()
    app.run(debug=True)
