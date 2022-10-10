from sqlalchemy import (
    Column,
    Integer,
    String,
)
from crawling.db.mysql_client import db_model


class Role(db_model):
    __tablename__ = "Role"
    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True)
    code = Column(String(200), unique=True)

    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code
