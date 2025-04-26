import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sec_summarizer.database.models import Base

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

DATABASE_URL = os.getenv(
    "DATABASE_URL", f"sqlite:///{os.path.join(REPO_ROOT, 'sec_summarizer.db')}"
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create the database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
