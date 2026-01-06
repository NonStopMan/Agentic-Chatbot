import redis.asyncio as redis
from typing import Optional
from app.core.config import settings

# Redis client instance
_redis_client: Optional[redis.Redis] = None


async def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    global _redis_client
    
    if _redis_client is None:
        _redis_client = await redis.from_url(
            settings.redis_url,
            db=settings.redis_db,
            encoding="utf-8",
            decode_responses=True,
        )
    
    return _redis_client


async def close_redis_client():
    """Close Redis client connection."""
    global _redis_client
    
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
