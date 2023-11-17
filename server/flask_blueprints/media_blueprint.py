import io
import json
import os.path
from pprint import pprint
import requests

from flask import Blueprint, request, Response, jsonify, send_file
from sqlalchemy.sql.expression import func

from constants import MAIN_DIR
from data_mapper.media_mapper import map_media
from db_loader import db
from sql_models.media_model import Media

bp = Blueprint('media', __name__)


@bp.route("/get")
def get():
    # parameters
    limit = request.args.get('limit', type=int)
    page = request.args.get('page', type=int)
    order = request.args.get('order')
    media_type = request.args.get('type')
    session_seed = request.args.get('session_seed', type=int)

    print(f'{limit =}', f'{order =}', f'{page =}', f'{media_type =}', f'{session_seed =}')

    # setup query
    query = (
        db.session.query(Media)
        .filter_by(media_type=media_type)
    )

    # order result
    match order:
        case 'release_date':
            query = query.order_by(Media.user_rating.desc(),
                                   Media.release_date.desc(),
                                   func.rand(session_seed),
                                   Media.id)
        case 'name':
            query = query.order_by(Media.user_rating.desc(),
                                   Media.name, func.rand(session_seed),
                                   Media.id)
        case _:
            query = query.order_by(Media.user_rating.desc(),
                                   func.rand(session_seed),
                                   Media.id)

    #     query = query.join(Card).order_by(Card.card_price.desc())
    #     query = query.join(CardTemplate).order_by(UserCard.storage_id, CARD_TYPE_PRIORITY, CardTemplate.name)

    # limiting
    if limit is not None:
        query = query.limit(limit).offset(page * limit)

    # get query and map
    media = query.all()
    mapped_media = map_media(media, media_type=media_type)

    return mapped_media


@bp.route("/get_image")
def get_image():
    media_id = request.args.get('id')
    file_path = os.path.join(MAIN_DIR, "assets", "poster_images_caches", f"{media_id}.jpg")

    # download locally if it doesn't exist
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        matched_media = db.session.query(Media).filter_by(id=media_id).one()
        response = requests.get(matched_media.poster_path)

        with open(file_path, 'wb') as outfile:
            outfile.write(response.content)

    return send_file(file_path, mimetype='image/jpg')

# @bp.route("/add_by_name")
# def add_by_name():
#     card_name = request.args.get('name')
#     print(f'searching for {card_name}')
#
#     found_cards = search_card_by_name(card_name)
#
#     new_card = UserCard(card_template_id=found_cards[0].id)
#
#     db.session.add(new_card)
#     db.session.commit()
#     db.session.close()
#
#     return []
#
#
# @bp.route("/delete")
# def delete():
#     card_id = request.args.get('id')
#     print(f'deleting {card_id}')
#
#     # db.session.update(UserCard).where(id=card_id).values(is_deleted=1)
#     db.session.query(UserCard).filter_by(id=card_id).delete()
#     db.session.commit()
#     db.session.close()
#
#     return []
#
#
# @bp.route("/set_card_attrib")
# def set_card_attrib():
#     user_card_id = request.args.get('user_card_id')
#     attr_name = request.args.get('attr_name')
#     attribute = request.args.get('attribute')
#
#     print(f'updating card {attr_name} of card {user_card_id} to {attribute}')
#
#     if attribute == 'null':
#         print('is null')
#         db.session.query(UserCard).filter_by(id=user_card_id).update({str(attr_name): None})
#     else:
#         db.session.query(UserCard).filter_by(id=user_card_id).update({str(attr_name): attribute})
#
#     db.session.commit()
#     db.session.close()
#
#     return []
#
#
# @bp.route("/search_by_name")
# def search_by_name():
#     card_name = request.args.get('name')
#
#     if card_name == '':
#         return []
#
#     print(f'searching for {card_name}')
#
#     found_cards = search_card_by_name(card_name)
#     found_cards_ids = [x.id for x in found_cards]
#
#     query = (
#         db.session
#         .query(UserCard)
#         .join(CardTemplate)
#         .filter(UserCard.card_template_id.in_(found_cards_ids))
#         # .filter(UserCard.storage_id.notin_([11]))
#         .order_by(UserCard.storage_id, CARD_TYPE_PRIORITY, CardTemplate.name)
#     )
#
#     cards_in_user = query.all()
#
#     mapped_cards = [map_card(uc) for uc in cards_in_user]
#
#     return mapped_cards
