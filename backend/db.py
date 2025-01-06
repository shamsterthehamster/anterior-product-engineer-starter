from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    """Dependency to get a database session"""
    db = Session()
    try:
        yield db
    finally:
        db.close()
