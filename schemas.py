from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    company: str

class UserCreate(UserBase):
    pass

# class UserUpdate(UserBase):
#     is_active: bool

class UserResponse(UserBase):
    id: int
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    company: Optional[str]
    is_active: Optional[bool]

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: str
    email: str
    phone: str
    company: str
    is_active: Optional[bool]