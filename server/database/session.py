from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from server.config import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass
