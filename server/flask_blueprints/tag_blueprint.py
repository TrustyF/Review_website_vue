import json

import sqlalchemy.exc
from flask import Blueprint, request, Response, jsonify, send_file
from db_loader import db
from sql_models.media_model import Tag

bp = Blueprint('tag', __name__)


@bp.route("/get", methods=['GET'])
def get():
    all_tags = db.session.query(Tag).all()

    return all_tags, 200


@bp.route("/add", methods=['POST'])
def add():
    data = request.get_json()
    del data['id']

    print(f'adding tag {data=}')

    new_tag = Tag(**data)
    db.session.add(new_tag)

    db.session.commit()

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return json.dumps({'ok': False}), 404, {'ContentType': 'application/json'}

    db.session.close()
    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}


@bp.route("/update", methods=['POST'])
def update():
    data = request.get_json()
    tag_id = data['id']
    del data['id']

    print(f'updating tag {data=}')

    db.session.query(Tag).filter(Tag.id == tag_id).update(data)

    db.session.commit()
    db.session.close()

    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}


@bp.route("/delete")
def delete():

    tag_id = request.args.get('id')

    print(f'deleting tag {tag_id=}')

    db.session.query(Tag).filter(Tag.id == tag_id).delete()

    db.session.commit()
    db.session.close()

    return json.dumps({'ok': True}), 200, {'ContentType': 'application/json'}
