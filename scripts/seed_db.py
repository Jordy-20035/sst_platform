"""
Run from project root:
python scripts/seed_db.py
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.db.base import Base
from backend.app.core.config import settings
from backend.app.models.user import User
from backend.app.models.incident import Incident
from backend.app.core.security import get_password_hash

DB_URL = settings.DATABASE_URL
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    try:
        # Create admin if not exists
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                full_name="Administrator",
                is_staff=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("Created admin user: admin / admin123")
        else:
            print("Admin exists already")

        # Add demo incidents
        if db.query(Incident).count() == 0:
            demo1 = Incident(
                title="Pothole near Central Park",
                description="Large pothole causing lane dodge",
                status="active",
                latitude=54.786, longitude=32.049
            )
            demo2 = Incident(
                title="Traffic jam on Lenina Ave",
                description="Accident causing heavy delays",
                status="reported",
                latitude=54.789, longitude=32.052
            )
            db.add_all([demo1, demo2])
            db.commit()
            print("Added demo incidents")
        else:
            print("Demo incidents already present")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    seed()
    print("Done.")

