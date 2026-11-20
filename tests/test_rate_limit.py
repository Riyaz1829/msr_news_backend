
import asyncio

from app.services.rate_limit import check_otp_rate_limit


async def main():
    mobile = "9876543210"

    for request_number in range(1, 7):
        allowed = await check_otp_rate_limit(mobile)

        print(
            f"Request {request_number}: "
            f"{'ALLOWED' if allowed else 'BLOCKED'}"
        )


asyncio.run(main())
