from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
)
import datetime
from crawling.db.mysql_client import db_model


class SpiderAuditErrors(db_model):
    __tablename__ = "SpiderAuditErrors"
    id = Column(Integer, primary_key=True)
    spiderName = Column(String(50))
    jobId = Column(String(100))
    errorField = Column(String(50))
    created_datetime = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_datetime = Column(
        DateTime(timezone=True), default=None, onupdate=datetime.datetime.utcnow
    )
    active = Column(Boolean)

    def __init__(self, spiderName, jobId, errorField, id=None, active=True):
        self.id = id
        self.spiderName = spiderName
        self.jobId = jobId
        self.errorField = errorField
        self.active = active
