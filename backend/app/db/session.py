from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from ..core.config import settings

# echo=True for debug if you want SQL logs
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


# Dependency to use in FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
