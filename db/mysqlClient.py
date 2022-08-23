from flask import Flask
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import importlib

from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from .jpa import *
load_dotenv('../.env.local')
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQL_CON']
engine = create_engine(os.getenv("SQL_CON"))
db_session  = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# dbM = SQLAlchemy(app)


# dbM.engine.create_all()
dbM = declarative_base()
dbM.query = db_session.query_property()
dbM.metadata.create_all(bind=engine)
_ = importlib.import_module("db.jpa.all_models")
dbM.metadata.create_all(bind=engine)
# define the function which will create your tables
# def init_db():
#     from .jpa import *
#     dbModel.metadata.create_all(bind=engine)
# init_db()