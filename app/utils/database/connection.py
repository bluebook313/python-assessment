from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas.config import DATABASE_URL
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

orm_session = sessionmaker(bind=engine)

Base = declarative_base() 



@contextmanager
def get_db():
    db = orm_session()

    try:
        yield db
    finally:
        db.close()