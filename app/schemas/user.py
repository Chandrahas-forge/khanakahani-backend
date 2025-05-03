from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True