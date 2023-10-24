from datetime import datetime
from dataclasses import dataclass

from db_loader import db


@dataclass
class TimeStampedModel(db.Model):
    __abstract__ = True

    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: datetime = db.Column(db.DateTime, onupdate=datetime.utcnow)

    is_deleted: bool = db.Column(db.Boolean)
