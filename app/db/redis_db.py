from aioredis import from_url, Redis

from config import REDIS_URL


async def redis_pool() -> Redis:
    # Create and return an async Redis client (connection pool)
    return await from_url(REDIS_URL, encoding='utf-8', decode_responses=True)
