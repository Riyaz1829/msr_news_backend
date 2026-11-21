
import hashlib
import hmac
import secrets

from app.core.redis import get_redis
from app.core.config import SECRET_KEY


OTP_EXPIRY = 300
OTP_MAX_ATTEMPTS = 5
VERIFICATION_EXPIRY = 600


# Generate a cryptographically secure six-digit OTP
def generate_otp() -> str:
    return str(secrets.randbelow(900000) + 100000)


# Use HMAC-SHA256 to protect OTP hashes with the server secret
def hash_otp(otp: str) -> str:
    return hmac.new(
        SECRET_KEY.encode("utf-8"),
        otp.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


# Store OTP and reset previous verification state atomically
STORE_OTP_SCRIPT = """
redis.call('DEL', KEYS[2], KEYS[3])

redis.call(
    'SET',
    KEYS[1],
    ARGV[1],
    'EX',
    ARGV[2]
)

return 1
"""


async def store_otp(mobile_number: str, otp: str) -> None:
    redis = await get_redis()

    key = f"otp:verification:{mobile_number}"
    attempts_key = f"otp:attempts:{mobile_number}"
    verified_key = f"otp:verified:{mobile_number}"

    await redis.eval(
        STORE_OTP_SCRIPT,
        3,
        key,
        attempts_key,
        verified_key,
        hash_otp(otp),
        OTP_EXPIRY
    )


# Verify OTP and enforce attempt limit atomically
VERIFY_OTP_SCRIPT = """
local otp_key = KEYS[1]
local attempts_key = KEYS[2]
local verified_key = KEYS[3]

local submitted_hash = ARGV[1]
local max_attempts = tonumber(ARGV[2])
local attempts_expiry = tonumber(ARGV[3])
local verification_expiry = tonumber(ARGV[4])

local stored_hash = redis.call('GET', otp_key)

if not stored_hash then
    return 0
end

local attempts = redis.call('INCR', attempts_key)

if attempts == 1 then
    redis.call('EXPIRE', attempts_key, attempts_expiry)
end

-- Correct OTP: allow verification, including on the fifth attempt
if stored_hash == submitted_hash then

    redis.call('DEL', otp_key, attempts_key)

    redis.call(
        'SET',
        verified_key,
        '1',
        'EX',
        verification_expiry
    )

    return 1
end

-- Fifth incorrect attempt: invalidate OTP immediately
if attempts >= max_attempts then
    redis.call('DEL', otp_key, attempts_key)
end

return 0
"""


async def verify_otp(mobile_number: str, otp: str) -> bool:
    redis = await get_redis()

    key = f"otp:verification:{mobile_number}"
    attempts_key = f"otp:attempts:{mobile_number}"
    verified_key = f"otp:verified:{mobile_number}"

    result = await redis.eval(
        VERIFY_OTP_SCRIPT,
        3,
        key,
        attempts_key,
        verified_key,
        hash_otp(otp),
        OTP_MAX_ATTEMPTS,
        OTP_EXPIRY,
        VERIFICATION_EXPIRY
    )

    return result == 1


# Consume verification marker exactly once
async def consume_mobile_verification(mobile_number: str) -> bool:
    redis = await get_redis()

    key = f"otp:verified:{mobile_number}"

    result = await redis.getdel(key)

    return result == "1"
