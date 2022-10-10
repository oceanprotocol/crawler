from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
)
import datetime
from crawling.db.mysql_client import db_model


class Target(db_model):
    __tablename__ = "Target"
    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True)
    code = Column(String(200), unique=True)
    is_active = Column(Boolean, default=True)  # soft delete
    created_datetime = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_datetime = Column(
        DateTime(timezone=True), default=None, onupdate=datetime.datetime.utcnow
    )

    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code
