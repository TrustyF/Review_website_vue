import datetime
from dataclasses import dataclass

from db_loader import db


# movie_genre_association = db.Table('movie_genre_association', TimeStampedModel.metadata,
#                                    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
#                                    db.Column('genre_id', db.Integer, db.ForeignKey('movie_genres.id'))
#                                    )


@dataclass
class MediaItem(db.Model):
    __tablename__ = "media_items"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(255), nullable=False)
    release_date: datetime.date = db.Column(db.Date)
    overview: str = db.Column(db.String(1000))
    poster_path: str = db.Column(db.String(100))

    media_type: str = db.Column(db.String(50), nullable=False)
    media_medium: str = db.Column(db.String(50), nullable=False)

    user_rating: int = db.Column(db.Integer, nullable=False)
    public_rating: float = db.Column(db.Float)

    is_dropped: bool = db.Column(db.Boolean)
    is_deleted: bool = db.Column(db.Boolean)
    created_at: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at: datetime.datetime = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    # genres = db.relationship("MovieGenre", secondary=movie_genre_association)

    __mapper_args__ = {'polymorphic_on': media_type}


@dataclass
class Movie(MediaItem):
    __mapper_args__ = {'polymorphic_identity': 'movie'}

    runtime: int = db.Column(db.Integer)

    imdb_id: str = db.Column(db.String(20), unique=True)


@dataclass
class Tv(MediaItem):
    __mapper_args__ = {'polymorphic_identity': 'tv'}

    imdb_id: str = db.Column(db.String(20), unique=True)

    episodes: int = db.Column(db.Integer)
    seasons: int = db.Column(db.Integer)


@dataclass
class Anime(MediaItem):
    __mapper_args__ = {'polymorphic_identity': 'anime'}

    imdb_id: str = db.Column(db.String(20), unique=True)

    episodes: int = db.Column(db.Integer)
    seasons: int = db.Column(db.Integer)


@dataclass
class Manga(MediaItem):
    __mapper_args__ = {'polymorphic_identity': 'manga'}

    content_rating: str = db.Column(db.String(50))


@dataclass
class Game(MediaItem):
    __mapper_args__ = {'polymorphic_identity': 'game'}

    hours_played: int = db.Column(db.Integer)

# @dataclass
# class Genre(TimeStampedModel):
#     __tablename__ = "genres"
#
#     id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name: str = db.Column(db.String(255), nullable=False, unique=True)
#
#     movies = db.relationship("Movie", secondary=movie_genre_association)
