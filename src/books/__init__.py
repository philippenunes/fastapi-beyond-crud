from src.books.routes import book_router as router

# Rebuild models to resolve forward references
from .schemas import BookDetailModel
from src.reviews.schemas import ReviewModel

BookDetailModel.model_rebuild()
