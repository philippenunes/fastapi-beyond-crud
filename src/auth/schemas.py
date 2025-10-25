from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(max_length=8)
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)


class UserModel(BaseModel):
    uid: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(max_length=8)
