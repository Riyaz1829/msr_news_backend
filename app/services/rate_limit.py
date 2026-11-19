
from app.core.redis import get_redis


OTP_RATE_LIMIT = 5
OTP_RATE_WINDOW = 3600


async def check_otp_rate_limit(mobile_number: str) -> bool:
    redis = await get_redis()

    key = f"otp:rate:{mobile_number}"

    # Increment and set expiry atomically
    lua_script = """
    local count = redis.call('INCR', KEYS[1])

    if count == 1 then
        redis.call('EXPIRE', KEYS[1], ARGV[1])
    end

    return count
    """

    count = await redis.eval(
        lua_script,
        1,
        key,
        OTP_RATE_WINDOW
    )

    return count <= OTP_RATE_LIMIT
