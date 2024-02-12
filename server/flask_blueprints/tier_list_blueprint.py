import json
from dataclasses import asdict

import sqlalchemy.exc
from flask import Blueprint, request, Response, jsonify, send_file
from sqlalchemy import func

from db_loader import db
from sql_models.media_model import Media, TierList
from flask_blueprints.login_blueprint import requires_auth

bp = Blueprint('tier_list', __name__)


@bp.route("/get", methods=['GET'])
def get():
    # all_tier_lists = db.session.query(TierList).all()

    tier_list_counts = (
        db.session.query(TierList, func.count(Media.id).label('count'))
        .outerjoin(TierList.media)
        .group_by(TierList)
        .all()
    )

    serialized_tier_lists = [{**asdict(tag), 'count': count} for tag, count in tier_list_counts]

    return serialized_tier_lists, 200


@bp.route("/add", methods=['GET'])
@requires_auth
def add():

    tier_list_name = request.args.get('name')

    # print(f'adding tier list {tier_list_name=}')

    new_tier_list = TierList(name=tier_list_name)
    db.session.add(new_tier_list)
    db.session.commit()

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return json.dumps({'ok': False}), 404, {'ContentType': 'application/json'}

    db.session.close()
    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}


# @bp.route("/update", methods=['POST'])
# def update():
#     data = request.get_json()
#     tag_id = data['id']
#
#     print(f'updating tag {data=}')
#
#     db.session.query(Tag).filter(Tag.id == tag_id).update({
#         'name': data['name'],
#         'overview': data['overview'],
#         'image_path': data['image_path'],
#         'tier': data['tier'],
#         'origin': data['origin'],
#     })
#
#     db.session.commit()
#     db.session.close()
#
#     return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}
#
#
# @bp.route("/delete")
# def delete():
#     tag_id = request.args.get('id')
#
#     print(f'deleting tag {tag_id=}')
#
#     db.session.query(Tag).filter(Tag.id == tag_id).delete()
#
#     db.session.commit()
#     db.session.close()
#
#     return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}
