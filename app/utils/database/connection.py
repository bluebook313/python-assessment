from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

orm_session = sessionmaker(bind=engine)


def get_db():
    db = orm_session()
    try:
        yield db
    finally:
        db.close()
