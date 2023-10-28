import datetime
from dataclasses import dataclass

from db_loader import db

media_genre_association = db.Table('media_genre_assoc', db.Model.metadata,
                                   db.Column('media_id', db.Integer, db.ForeignKey('medias.id')),
                                   db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'))
                                   )

media_theme_association = db.Table('media_theme_assoc', db.Model.metadata,
                                   db.Column('media_id', db.Integer, db.ForeignKey('medias.id')),
                                   db.Column('theme_id', db.Integer, db.ForeignKey('themes.id'))
                                   )

media_tag_association = db.Table('media_tag_assoc', db.Model.metadata,
                                 db.Column('media_id', db.Integer, db.ForeignKey('medias.id')),
                                 db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                                 )


@dataclass
class Genre(db.Model):
    __tablename__ = "genres"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(50), nullable=False, unique=True)
    origin: str = db.Column(db.String(50), nullable=False)

    media = db.relationship("Media", secondary=media_genre_association)


@dataclass
class Theme(db.Model):
    __tablename__ = "themes"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(50), nullable=False, unique=True)
    origin: str = db.Column(db.String(50), nullable=False)

    media = db.relationship("Media", secondary=media_theme_association)


@dataclass
class Tag(db.Model):
    __tablename__ = "tags"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(50), nullable=False, unique=True)
    overview: str = db.Column(db.String(1000))
    image_path: str = db.Column(db.String(100))
    tier: str = db.Column(db.String(100))
    origin: str = db.Column(db.String(50), nullable=False)

    media = db.relationship("Media", secondary=media_tag_association)


@dataclass
class Media(db.Model):
    __tablename__ = "medias"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(255), nullable=False)
    release_date: datetime.date = db.Column(db.Date)
    overview: str = db.Column(db.String(1000))
    poster_path: str = db.Column(db.String(100))

    media_type: str = db.Column(db.String(50), nullable=False)
    media_medium: str = db.Column(db.String(50))

    user_rating: int = db.Column(db.Integer, nullable=False)
    public_rating: float = db.Column(db.Float)

    is_dropped: bool = db.Column(db.Boolean)
    is_deleted: bool = db.Column(db.Boolean)
    created_at: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at: datetime.datetime = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    external_id: str = db.Column(db.String(100), unique=True)

    runtime: int = db.Column(db.Integer)
    episodes: int = db.Column(db.Integer)
    seasons: int = db.Column(db.Integer)
    content_rating: str = db.Column(db.String(50))

    genres = db.relationship("Genre", secondary=media_genre_association)
    themes = db.relationship("Theme", secondary=media_theme_association)
    tags = db.relationship("Tag", secondary=media_tag_association)
