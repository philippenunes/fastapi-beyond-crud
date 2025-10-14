from typing import Optional
from pydantic import BaseModel

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    publisher: str
    published_at: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str