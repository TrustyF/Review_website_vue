from db_loader import db
from sql_models.media_model import Movie


def map_movie(movie):
    movie = db.session.query(Movie).filter_by(id=movie.id).one_or_none()

    return movie
