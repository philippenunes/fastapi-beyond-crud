from src.auth.routes import auth_router as router

# Rebuild models to resolve forward references
from .schemas import UserBooksModel
from src.books.schemas import Book
from src.reviews.schemas import ReviewModel

UserBooksModel.model_rebuild()
