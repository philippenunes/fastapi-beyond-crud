from fastapi import FastAPI
from src.books import router as book_router
from src.auth import router as auth_router
from src.reviews import router as reviews_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import register_all_errors


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"server is starting...")
    await init_db()
    yield
    print(f"server has been stopped")


version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
)

# Permite requisições de qualquer origem (apenas para desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_all_errors(app)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(reviews_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
