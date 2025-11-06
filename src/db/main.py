from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import re
import ssl

async_engine = create_async_engine(
    re.sub(r"^postgresql:", "postgresql+asyncpg:", Config.DATABASE_URL),
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "ssl": ssl.create_default_context(),
        "server_settings": {"jit": "off"},
    },
)


async def init_db():
    from src.books.models import Book
    from src.auth.models import User

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session
