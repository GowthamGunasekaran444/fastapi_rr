from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Define the database URL. Using SQLite for simplicity.
# This will create a 'chatbot.db' file in the project root.
DATABASE_URL = "sqlite:///./chatbot.db"

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed for SQLite
# when using multiple threads (like FastAPI's default Uvicorn workers).
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
# Each instance of SessionLocal will be a database session.
# The `autocommit=False` means we need to explicitly commit changes.
# The `autoflush=False` means objects won't be flushed to the database until commit or query.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our declarative models
Base = declarative_base()

def get_db():
    """
    Dependency function to get a database session.
    This will be used by FastAPI's Depends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_all_tables():
    """
    Creates all defined tables in the database.
    Call this function once when the application starts.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created or already exist.")