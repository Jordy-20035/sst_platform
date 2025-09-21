from sqlalchemy.orm import Session
from ..models.user import User
from ..core.security import get_password_hash


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, password: str, full_name: str | None = None, is_staff: bool = False) -> User:
    hashed = get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed, full_name=full_name, is_staff=is_staff)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
