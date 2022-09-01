from sqlalchemy import Boolean, Column, Integer, String,  \
     DateTime, ForeignKey, JSON
import datetime
from crawling.db.mysqlClient import dbM
from sqlalchemy.orm import relationship

class Client(dbM):
    __tablename__ = 'Client'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True)
    code = Column(String(200), unique=True)
    is_active = Column(Boolean, default=True)  # soft delete
    created_datetime = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_datetime = Column(DateTime(timezone=True), default=None, onupdate=datetime.datetime.utcnow)

    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code

class Role(dbM):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True)
    code = Column(String(200), unique=True)

    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code

class User(dbM):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    firstName = Column(String(30))
    lastName = Column(String(30))
    active = Column(Boolean)
    role_id = Column(Integer, ForeignKey('Role.id'))
    role = relationship("Role")
    def __init__(self, id=None, firstName=None, lastName=None, role_id=None, role=None):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.role_id = role_id
        self.role = role

class Data(dbM):
    __tablename__ = 'Data'
    id = Column(Integer, primary_key=True)
    info = Column(JSON)
    active = Column(Boolean)

    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship("User")

    client_id = Column(Integer, ForeignKey('Client.id'))
    client = relationship("Client")

    def __init__(self, id=None, info=None, active=None, user_id=None, user=None, client_id=None, client=None):
        self.id = id
        self.info = info
        self.lastName = active
        self.user_id = user_id
        self.user = user
        self.client_id = client_id
        self.client = client