import datetime
from sql_models.base_model import TimeStampedModel
from dataclasses import dataclass

from db_loader import db

movie_genre_association = db.Table('movie_genre_association', TimeStampedModel.metadata,
                                   db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
                                   db.Column('genre_id', db.Integer, db.ForeignKey('movie_genres.id'))
                                   )


@dataclass
class Movie(TimeStampedModel):
    __tablename__ = "movies"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(255), nullable=False)
    overview: str = db.Column(db.String(1000))
    poster_path: str = db.Column(db.String(50))
    release_date: datetime.date = db.Column(db.Date)
    runtime: int = db.Column(db.Integer)
    imdb_id: int = db.Column(db.String(20), unique=True)
    media_type: str = db.Column(db.String(50), nullable=False)

    user_rating: int = db.Column(db.Integer, nullable=False)
    public_rating: float = db.Column(db.Float)

    genres = db.relationship("MovieGenre", secondary=movie_genre_association)

    # card_id: int = db.Column(db.Integer, db.ForeignKey('Cards.id', ondelete='CASCADE'))
    # card = db.relationship("Card", back_populates="users", passive_deletes=True)


@dataclass
class MovieGenre(TimeStampedModel):
    __tablename__ = "movie_genres"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(255), nullable=False, unique=True)

    movies = db.relationship("Movie", secondary=movie_genre_association)
