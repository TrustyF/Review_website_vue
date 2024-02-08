from dataclasses import asdict
from datetime import datetime
from sqlalchemy import func
from db_loader import db
from sql_models.media_model import Media, ContentRating, TierList


def serialize_media(media):
    def calc_scaled_rating():

        def remap_value(value, old_min, old_max, new_min, new_max):
            if None in (value, old_min, old_max, new_min, new_max):
                return 0

            if value < old_min:
                return value
            if value > old_max:
                return value

            old_range = (old_max - old_min)
            new_range = (new_max - new_min)
            new_value = (((value - old_min) * new_range) / old_range) + new_min
            return new_value

        pub_rating_min = (db.session.query(func.min(Media.public_rating))
                          .where(Media.media_type == media.media_type)
                          .where(Media.public_rating > 0)
                          .scalar())
        pub_rating_max = (db.session.query(func.max(Media.public_rating))
                          .where(Media.media_type == media.media_type)
                          .scalar())
        user_rating_min = (db.session.query(func.min(Media.user_rating))
                           .where(Media.media_type == media.media_type)
                           .scalar())
        user_rating_max = 10

        return remap_value(media.public_rating,
                           pub_rating_min,
                           pub_rating_max,
                           user_rating_min,
                           user_rating_max) \
            if (pub_rating_min <= 7 if pub_rating_min is not None else False) else media.public_rating

    return {
        'id': media.id,
        'name': media.name,
        'external_name': media.external_name,
        'release_date': media.release_date.isoformat() if media.release_date is not None else None,
        'overview': media.overview,
        'poster_path': media.poster_path,
        'author': media.author,
        'studio': media.studio,
        'media_type': media.media_type,
        'media_medium': media.media_medium,
        'user_rating': media.user_rating,
        'public_rating': media.public_rating,
        'scaled_public_rating': calc_scaled_rating(),
        'is_dropped': media.is_dropped,
        'is_deleted': media.is_deleted,
        'created_at': media.created_at,
        'updated_at': media.updated_at,
        'external_id': media.external_id,
        'external_link': media.external_link,
        'video_link': media.video_link,
        'content_rating': media.content_rating or ContentRating(),
        'runtime': media.runtime,
        'episodes': media.episodes,
        'seasons': media.seasons,

        'genres': media.genres,
        'themes': media.themes,
        'tags': [x for x in media.tags if x.is_deleted is not True],
        'tier_lists': media.tier_lists,
    }


def deserialize_media(data):
    return {
        'name': data.get('name'),
        'external_name': data.get('external_name'),
        'release_date': datetime.strptime(data.get('release_date'), '%Y-%m-%d'),
        'overview': data.get('overview')[:1000] if data.get('overview') else None,
        'poster_path': data.get('poster_path'),
        'author': data.get('author'),
        'studio': data.get('studio'),
        'media_type': data.get('media_type'),
        'media_medium': data.get('media_medium'),
        'user_rating': data.get('user_rating'),
        'public_rating': data.get('public_rating'),
        'is_dropped': data.get('is_dropped'),
        'is_deleted': data.get('is_deleted'),
        'external_id': data.get('external_id'),
        'external_link': data.get('external_link'),
        'video_link': data.get('video_link'),
        'runtime': data.get('runtime'),
        'episodes': data.get('episodes'),
        'seasons': data.get('seasons'),
    }
