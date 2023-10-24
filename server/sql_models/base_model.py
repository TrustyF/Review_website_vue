from datetime import datetime
from dataclasses import dataclass

from db_loader import db


class TimeStampedModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    is_deleted = db.Column(db.Boolean)
