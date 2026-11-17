
import asyncio
from sqlalchemy import text

from app.database.async_session import AsyncSessionLocal


async def test_session():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        print("Async session working:", result.scalar())


if __name__ == "__main__":
    asyncio.run(test_session())
