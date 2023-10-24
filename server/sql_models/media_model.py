import datetime
from sql_models.base_model import TimeStampedModel
from dataclasses import dataclass

from db_loader import db


@dataclass
class Movie(TimeStampedModel):
    __tablename__ = "Movies"

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

    def __repr__(self):
        return f" {self.movie_template_id}-{self.__class__.__name__},name: {self.name}"

@dataclass
class MovieGenre(TimeStampedModel):
    __tablename__ = "MovieGenres"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(255), nullable=False)

    
@dataclass
class MovieGenre(TimeStampedModel):
    __tablename__ = "MovieGenres"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(255), nullable=False)