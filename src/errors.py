from typing import Any, Callable
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class BooklyException(Exception):
    """This is the base class for all bookly errors"""

    pass


class InvalidToken(BooklyException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(BooklyException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(BooklyException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(BooklyException):
    """User has provided an access token when a refresh token is needed"""

    pass


class UserAlreadyExists(BooklyException):
    """User has provided an email for a user who exists during sign up."""

    pass


class InvalidCredentials(BooklyException):
    """User has provided wrong email or password during log in."""

    pass


class InsufficientPermission(BooklyException):
    """User does not have the neccessary permissions to perform an action."""

    pass


class BookNotFound(BooklyException):
    """Book Not found"""

    pass


class UserNotFound(BooklyException):
    """User Not found"""

    pass


class AccountNotVerified(Exception):
    """Account not yet verified"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exeption_handler(request: Request, exc: BooklyException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exeption_handler


def register_all_errors(app: FastAPI) -> None:
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

    async def internal_server_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    app.add_exception_handler(500, internal_server_error_handler)
