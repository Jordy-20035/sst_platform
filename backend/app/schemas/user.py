from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str | None = None


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str | None = None
    is_active: bool
    is_staff: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
