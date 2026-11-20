import asyncio
from app.core.redis import get_redis

async def main():
    redis = await get_redis()

    response = await redis.ping()
    print("Redis connection successful:", response)

    await redis.set("msr_test", "Hello MSR News")
    value = await redis.get("msr_test")

    print("Redis stored value:", value)

asyncio.run(main())