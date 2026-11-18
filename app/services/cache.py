import json

from app.core.redis import get_redis

CACHE_TTL = 86400  # 24 hours


async def set_cache(key: str, data, ttl: int = CACHE_TTL):
    redis = await get_redis()
    value = json.dumps(data)
    await redis.set(key, value, ex=ttl)


async def get_cache(key: str):
    redis = await get_redis()
    value = await redis.get(key)

    if value is None:
        return None

    return json.loads(value)


async def delete_cache(key: str):
    redis = await get_redis()
    await redis.delete(key)