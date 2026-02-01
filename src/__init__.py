from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books import router as book_router
from src.auth import router as auth_router
from src.reviews import router as reviews_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.db.main import init_db
from .erros import (
    create_exception_handler,
    InvalidCredentials,
    BookNotFound,
    UserAlreadyExists,
    UserNotFound,
    InsufficientPermission,
    AccessTokenRequired,
    InvalidToken,
    RefreshTokenRequired,
    RevokedToken,
    AccountNotVerified,
)


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

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User already exists",
            "error_code": "user_exists",
            "resolution": "Use a different email address or log in.",
        },
    ),
)

app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "User not found",
            "error_code": "user_not_found",
            "resolution": "Verify the user ID or email and try again.",
        },
    ),
)

app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Book not found",
            "error_code": "book_not_found",
            "resolution": "Verify the book ID and try again.",
        },
    ),
)

app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Invalid credentials",
            "error_code": "invalid_credentials",
            "resolution": "Check your email and password and try again.",
        },
    ),
)

app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Invalid token",
            "error_code": "invalid_token",
            "resolution": "Log in again to get a new token.",
        },
    ),
)

app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Token has been revoked",
            "error_code": "token_revoked",
            "resolution": "Log in again to get a new token.",
        },
    ),
)

app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Access token required",
            "error_code": "access_token_required",
            "resolution": "Include a valid access token in the Authorization header.",
        },
    ),
)

app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Refresh token required",
            "error_code": "refresh_token_required",
            "resolution": "Use a refresh token for this endpoint.",
        },
    ),
)

app.add_exception_handler(
    InsufficientPermission,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Insufficient permission",
            "error_code": "insufficient_permission",
            "resolution": "Request the required permissions or use a different account.",
        },
    ),
)

app.add_exception_handler(
    AccountNotVerified,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Account not verified",
            "error_code": "account_not_verified",
            "resolution": "Verify your account and try again.",
        },
    ),
)


@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        content={"message": "Oops! Something went wrong", "error_code": "server_error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(reviews_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
