from flask import Blueprint, request, Response, jsonify, send_file
from db_loader import db
from sql_models.media_model import Tag

bp = Blueprint('tag', __name__)


@bp.route("/get", methods=['GET'])
def get():
    request.args.get('media_type')

    all_tags = db.session.query(Tag).all()

    return all_tags,200
