from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
    UniqueConstraint,
)
import datetime

from crawling.db.jpa.target import Target
from crawling.db.jpa.user import User
from crawling.db.mysql_client import db_model
from sqlalchemy.orm import relationship


class Data(db_model):
    __tablename__ = "Data"
    id = Column(Integer, primary_key=True)
    info = Column(JSON)
    active = Column(Boolean)
    url = Column(String(100))
    sha = Column(String(100))
    user_id = Column(Integer, ForeignKey("User.id"))
    user = relationship(User)

    target_id = Column(Integer, ForeignKey("Target.id"))
    target = relationship(Target)
    created_datetime = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_datetime = Column(
        DateTime(timezone=True), default=None, onupdate=datetime.datetime.utcnow
    )
    __table_args__ = (UniqueConstraint("sha", "url", name="_sha_ulr_uc"),)

    def __init__(
        self,
        id=None,
        info=None,
        active=None,
        user_id=None,
        user=None,
        target_id=None,
        target=None,
        url=None,
        sha=None,
    ):
        self.id = id
        self.info = info
        self.lastName = active
        self.user_id = user_id
        self.user = user
        self.target_id = target_id
        self.target = target
        self.url = url
        self.sha = sha
