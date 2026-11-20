import asyncio

from app.services.cache import set_cache, get_cache, delete_cache


async def main():
    sample_districts = [
        {"id": 1, "name": "Hyderabad"},
        {"id": 2, "name": "Rangareddy"}
    ]

    await set_cache("test:districts", sample_districts)

    result = await get_cache("test:districts")
    print("Cached districts:", result)

    await delete_cache("test:districts")

    result = await get_cache("test:districts")
    print("After deletion:", result)


asyncio.run(main())