from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base

# Creating database and engine and opening a session
engine = create_engine("sqlite:///database/database.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables in the database
Base.metadata.create_all(engine)
