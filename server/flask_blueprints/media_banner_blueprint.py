from flask import Blueprint, request
from sqlalchemy import or_,not_

from app import cache
from data_mapper.serializer import serialize_media
from db_loader import db
from sql_models.media_model import Media

bp = Blueprint('media_banner', __name__)


@bp.route("/recent_watch", methods=['POST'])
@cache.cached()
def get_recent_watch():
    # parameters
    data = request.get_json()
    limit = data.get('limit')
    page = data.get('page')
    media_types = data.get('types')

    # setup query
    query = (db.session.query(Media).filter(
        or_(Media.is_deleted == 0, Media.is_deleted == None)))  # noqa

    if media_types and len(media_types) > 0:
        if 'all' not in media_types:
            query = query.filter(Media.media_type.in_(media_types))

    # filter recent releases to avoid dupes
    recent_releases_subquery = (
        db.session.query(Media.id)
        .order_by(Media.release_date.desc())
        .limit(20)
        .subquery()
    )

    query = query.filter(not_(Media.id.in_(recent_releases_subquery.select())))

    query = query.order_by(Media.created_at.desc())

    # limiting
    if limit is not None:
        query = query.limit(limit).offset(page * limit)

    # get query and map
    media = query.all()
    serialized_media = [serialize_media(x) for x in media]

    return {
        'media': serialized_media,
        'matched_field': None,
    }, 200


@bp.route("/recent_release", methods=['POST'])
@cache.cached()
def get_recent_release():
    # parameters
    data = request.get_json()
    limit = data.get('limit')
    page = data.get('page')
    media_types = data.get('types')

    # setup query
    query = (db.session.query(Media).filter(
        or_(Media.is_deleted == 0, Media.is_deleted == None)))  # noqa

    if media_types and len(media_types) > 0:
        if 'all' not in media_types:
            query = query.filter(Media.media_type.in_(media_types))

    query = query.order_by(Media.release_date.desc())

    # limiting
    if limit is not None:
        query = query.limit(limit).offset(page * limit)

    # get query and map
    media = query.all()
    serialized_media = [serialize_media(x) for x in media]

    return {
        'media': serialized_media,
        'matched_field': None,
    }, 200
