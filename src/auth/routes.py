from fastapi import APIRouter, status, HTTPException, Depends
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token, verify_password
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from .dependencies import RefreshTokenBearer

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRE_DAYS = 2


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    if await user_service.user_exists(email, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )

    user = await user_service.create_user(user_data, session)
    return user


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiration=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "user": {"uid": str(user.uid), "email": user.email},
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "message": "Login successful",
                },
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid email or password.",
    )


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details=Depends(RefreshTokenBearer())):
    expiration_timestamp = token_details["exp"]

    if expiration_timestamp > datetime.now().timestamp():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": new_access_token,
                "message": "New access token generated successfully",
            },
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalide or expired refresh token.",
    )
