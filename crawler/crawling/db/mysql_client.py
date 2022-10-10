import os
from sqlalchemy import create_engine, MetaData

from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker


engine = create_engine(os.getenv("MYSQL_CON"), pool_size=20, max_overflow=0)
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))


db_model = declarative_base()
db_model.query = db_session.query_property()


def db_initialization():
    db_model.metadata.reflect(bind=engine)
    db_model.metadata.create_all(bind=engine)
