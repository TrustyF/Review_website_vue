import json
from dataclasses import asdict

import sqlalchemy.exc
from flask import Blueprint, request
from sqlalchemy import func

from app import cache
from db_loader import db
from sql_models.media_model import Media, UserList
from flask_blueprints.login_blueprint import requires_auth

bp = Blueprint('user_list', __name__)


@bp.route("/get", methods=['GET'])
@cache.cached()
def get():

    user_counts = (
        db.session.query(UserList, func.count(Media.id).label('count'))
        .outerjoin(UserList.media)
        .group_by(UserList)
        .all()
    )

    serialized_user = [{**asdict(user), 'count': count} for user, count in user_counts]

    return serialized_user, 200


@bp.route("/add", methods=['GET'])
@requires_auth
def add():
    user_name = request.args.get('name')

    new_user = UserList(name=user_name)
    db.session.add(new_user)
    db.session.commit()

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return json.dumps({'ok': False}), 404, {'ContentType': 'application/json'}

    db.session.close()
    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}
