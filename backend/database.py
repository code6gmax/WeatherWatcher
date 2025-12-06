from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 1. Get the Database URL from the environment (Render provides this automatically)
# If not found, fallback to a local SQLite file for testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./weather.db")

# Fix for Render: The URL sometimes starts with "postgres://", but SQLAlchemy needs "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. Create the Database Engine
engine = create_engine(DATABASE_URL)

# 3. Create a SessionLocal class
# Each request will create a new session instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class for our models
Base = declarative_base()

# 5. Dependency helper to get the DB session in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()