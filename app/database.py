import os

from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    (
        "postgresql+psycopg://opportunity_user:"
        "opportunity_password@localhost:5433/product_opportunity"
    ),
)

class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
     bind=engine,
     autoflush=False,
     expire_on_commit = False,
)

def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()