from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from ...db.session import get_db
from ...schemas.user import UserCreate, Token, UserOut
from ...crud.user import get_user_by_username, create_user
from ...core.security import verify_password, create_access_token
from ...core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = create_user(db, username=user_in.username, password=user_in.password, full_name=user_in.full_name)
    return user


class LoginRequest(UserCreate):
    password: str


@router.post("/login", response_model=Token)
def login(form: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}
