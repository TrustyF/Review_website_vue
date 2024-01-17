from flask import Blueprint, request, Response, jsonify, send_file

bp = Blueprint('tag', __name__)


@bp.route("/get", methods=['GET'])
def get():
    pass
