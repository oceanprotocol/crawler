import sqlalchemy as sa

from db.mysqlClient import dbM
from sqlalchemy.orm import relationship

class Client(dbM):
    __tablename__ = 'Client'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(10), unique=True)
    code = sa.Column(sa.String(200), unique=True)

    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code

class Role(dbM):
    __tablename__ = 'Role'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(10), unique=True)
    code = sa.Column(sa.String(200), unique=True)

    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code

class User(dbM):
    __tablename__ = 'User'
    id = sa.Column(sa.Integer, primary_key=True)
    firstName = sa.Column(sa.String(30))
    lastName = sa.Column(sa.String(30))
    active = sa.Column(sa.Boolean)
    role_id = sa.Column(sa.Integer, sa.ForeignKey('Role.id'))
    role = relationship("Role")
    def __init__(self, id=None, firstName=None, lastName=None, role_id=None, role=None):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.role_id = role_id
        self.role = role

class Data(dbM):
    __tablename__ = 'Data'
    id = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.JSON)
    active = sa.Column(sa.Boolean)

    user_id = sa.Column(sa.Integer, sa.ForeignKey('User.id'))
    user = relationship("User")

    client_id = sa.Column(sa.Integer, sa.ForeignKey('Client.id'))
    client = relationship("Client")

    def __init__(self, id=None, firstName=None, lastName=None, user_id=None, user=None, client_id=None, client=None):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.user_id = user_id
        self.user = user
        self.client_id = client_id
        self.client = client