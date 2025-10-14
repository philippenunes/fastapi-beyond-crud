from fastapi import FastAPI
from src.books import router as book_router
from fastapi.middleware.cors import CORSMiddleware  

version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version = version
)

# Permite requisições de qualquer origem (apenas para desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
