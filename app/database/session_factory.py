from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base

# Create engine and tables
engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(engine)

# Tie the engine to the session returned
SessionFactory = sessionmaker(bind=engine)


def get_session():
    return SessionFactory()
