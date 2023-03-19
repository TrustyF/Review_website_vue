from flask import Flask, request, Response
# from flask_cors import CORS, cross_origingg

import functions

app = Flask(__name__)


# CORS(app)


# routes
@app.route('/get_movies/', methods=["GET"])
# @cross_origin()
def get_movies():
    return functions.get_all_movies()


@app.route('/edit_movie/', methods=["POST"])
# @cross_origin()
def edit_movie():
    functions.edit_movie(request.json)
    return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True)
