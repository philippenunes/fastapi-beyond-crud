from __future__ import annotations
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.books.schemas import Book
    from src.reviews.schemas import ReviewModel


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


class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(max_length=8)
