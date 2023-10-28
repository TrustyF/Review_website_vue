from db_loader import db
from sql_models.media_model import Media


def map_movie(movie):
    movie = db.session.query(Media).filter_by(id=movie.id).one_or_none()

    return movie
