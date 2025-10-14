from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Permite requisições de qualquer origem (apenas para desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "publisher": "Secker & Warburg", "published_at": "1949-06-08", "page_count": 328, "language": "English"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "publisher": "J.B. Lippincott & Co.", "published_at": "1960-07-11", "page_count": 281, "language": "English"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "publisher": "Charles Scribner's Sons", "published_at": "1925-04-10", "page_count": 180, "language": "English"}
]

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

@app.get('/books', response_model=List[Book])
async def get_all_books():
    return books

@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book) -> dict:
    new_book = book.model_dump()

    books.append(new_book)
    return {"message": "Book created successfully", "book": new_book}

@app.get('/books/{book_id}')
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )

@app.patch('/books/{book_id}')
async def update_book(book_id: int, book_update: BookUpdateModel) -> dict:
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update.title
            book["author"] = book_update.author            
            book["publisher"] = book_update.publisher
            book["page_count"] = book_update.page_count
            book["language"] = book_update.language

            return book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )

@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int) -> None:
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )