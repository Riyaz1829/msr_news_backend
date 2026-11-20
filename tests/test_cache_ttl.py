
import asyncio
from app.services.cache import set_cache, get_cache

async def main():
    key = "msr:ttl:test"

    await set_cache(
        key,
        {"message": "Testing cache expiry"},
        ttl=5
    )

    result = await get_cache(key)
    print("Before expiry:", result)

    await asyncio.sleep(6)

    expired_result = await get_cache(key)
    print("After expiry:", expired_result)

    assert expired_result is None, "Cache key did not expire!"
    print("TTL expiry test passed!")

asyncio.run(main())
