import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base

# Create engine and tables
db_uri = os.getenv("DATABASE_URI", "sqlite:////results/database.db")
engine = create_engine(db_uri, echo=True)
Base.metadata.create_all(engine)

# Tie the engine to the session returned
SessionFactory = sessionmaker(bind=engine)


def get_session():
    return SessionFactory()
