from redis import asyncio
from src.config import Config

JTI_EXPIRE_SECONDS = 3600  # 1 hour

token_blacklist = asyncio.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    decode_responses=True,  # Retorna strings ao invés de bytes
)


async def add_jti_to_blacklist(jti: str) -> None:
    await token_blacklist.set(name=jti, value="", ex=JTI_EXPIRE_SECONDS)


async def token_in_blacklist(jti: str) -> bool:
    token = await token_blacklist.get(jti)
    return token is not None
