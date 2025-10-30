from fastapi import APIRouter, status, Depends
from typing import List
from fastapi.exceptions import HTTPException
from src.books.schemas import Book, BookUpdateModel
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from .service import BookService
from .schemas import BookCreateModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(allowed_roles=["admin", "user"]))


@book_router.get("/", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> List[Book]:

    print(user_details)
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_book(
    book: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    new_book = await book_service.create_book(book, session)
    return {"message": "Book created successfully", "book": new_book}


@book_router.get("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.patch("/{book_uid}", dependencies=[role_checker])
async def update_book(
    book_uid: str,
    book_update: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    update_book = await book_service.update_book(book_uid, book_update, session)
    if update_book:
        return {"message": "Book updated successfully", "book": update_book}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete(
    "/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> None:
    book_deleted = await book_service.delete_book(book_uid, session)
    if book_deleted:
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
