from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.config import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
