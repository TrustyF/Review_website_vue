from flask import Flask, Request, request, Response
from flask_cors import CORS

import functions

app = Flask(__name__)
CORS(app)


# routes
@app.route('/get_movies/', methods=["POST"])
def get_movies():
    return functions.get_all_movies(request.json)


# @app.route('/edit_movie/', methods=["POST"])
# def edit_movie():
#     functions.edit_movie(request.json)
#     return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True)
