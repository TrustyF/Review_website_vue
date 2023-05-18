from flask import Flask, Request, request, Response
from flask_cors import CORS

from storage import store

app = Flask(__name__)
CORS(app)


# routes
@app.route('/set_media_type', methods=["POST"])
def set_media_type():
    store.set_current_media(request.json['media_type'])
    return Response(status=200)


@app.route('/set_settings', methods=["POST"])
def set_settings():
    store.get_curr_media().set_settings(request.json)
    return Response(status=200)


@app.route('/set_filters', methods=["POST"])
def set_filters():
    store.get_curr_media().set_filters(request.json)
    return Response(status=200)


@app.route('/get_media', methods=["GET"])
def get_media():
    return store.get_curr_media().get_all_media()


@app.route('/load_more', methods=["POST"])
def load_more():
    return store.get_curr_media().load_more()


# @app.route('/get_recent_movie_ratings/', methods=["GET", "POST"])
# def get_recent_movie_ratings():
#     return functions.get_recent_movie_ratings(request.json)
#
#
@app.route('/add_media/', methods=["POST"])
def add_media():
    store.get_curr_media().add_media(request.json)
    return Response(status=200)


@app.route('/update_media/', methods=["POST"])
def update_media():
    store.get_curr_media().update_media(request.json)
    return Response(status=200)


@app.route('/del_media/', methods=["POST"])
def del_media():
    store.get_curr_media().del_media(request.json)
    return Response(status=200)


#
#
# @app.route('/get_presets/', methods=["GET"])
# def get_presets():
#     return functions.get_all_presets()
#
#
# @app.route('/add_preset/', methods=["POST"])
# def add_preset():
#     functions.add_preset(request.json)
#     return Response(status=200)
#
#
# @app.route('/del_preset/', methods=["POST"])
# def del_preset():
#     functions.del_preset(request.json)
#     return Response(status=200)
#
#
# @app.route('/check_dupe/', methods=["POST"])
# def check_dupe():
#     state = functions.check_dupe(request.json)
#     return Response(status=200), state


if __name__ == '__main__':
    app.run(debug=True)
