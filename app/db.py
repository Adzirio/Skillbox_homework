from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

Base = declarative_base()
session = None
engine = None


def init_db(uri: str):
    global engine, session
    engine = create_engine(uri, echo=False)
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    Base.query = session.query_property()
    return engine


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()
