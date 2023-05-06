from flask import Flask, Request, request, Response
from flask_cors import CORS

import functions

app = Flask(__name__)
CORS(app)


# routes
@app.route('/get_movies/', methods=["GET", "POST"])
def get_movies():
    return functions.get_all_movies(request.json)


@app.route('/edit_movie/', methods=["POST"])
def edit_movie():
    functions.edit_movie(request.json)
    return Response(status=200)


@app.route('/add_movie/', methods=["POST"])
def add_movie():
    functions.add_movie(request.json)
    return Response(status=200)


@app.route('/del_movie/', methods=["POST"])
def del_movie():
    functions.del_movie(request.json)
    return Response(status=200)


@app.route('/get_presets/', methods=["GET"])
def get_presets():
    return functions.get_all_presets()


@app.route('/add_preset/', methods=["POST"])
def add_preset():
    functions.add_preset(request.json)
    return Response(status=200)


@app.route('/del_preset/', methods=["POST"])
def del_preset():
    functions.del_preset(request.json)
    return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True)
    # functions.reset_db()
