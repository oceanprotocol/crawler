from flask import Flask
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import importlib

from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from .jpa import *
engine = create_engine(os.getenv("SQL_CON"))
db_session  = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


dbM = declarative_base()
dbM.query = db_session.query_property()
_ = importlib.import_module("crawling.db.jpa.all_models")
dbM.metadata.create_all(bind=engine)