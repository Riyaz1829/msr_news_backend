import asyncio

from app.services.msg91 import msg91_service


async def main():

    result = await msg91_service.send_otp(
        mobile_number="9876543210",
        otp="123456"
    )

    print("MSG91 Mock Test Result:")
    print(result)


asyncio.run(main())