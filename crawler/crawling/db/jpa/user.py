from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
)

from crawling.db.jpa.role import Role
from crawling.db.mysql_client import db_model
from sqlalchemy.orm import relationship


class User(db_model):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    firstName = Column(String(30))
    lastName = Column(String(30))
    active = Column(Boolean)
    role_id = Column(Integer, ForeignKey("Role.id"))
    role = relationship(Role)

    def __init__(self, id=None, firstName=None, lastName=None, role_id=None, role=None):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.role_id = role_id
        self.role = role
