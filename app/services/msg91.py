
import re


class MSG91Service:

    def __init__(self):
        self.provider = "mock"

    async def send_otp(
        self,
        mobile_number: str,
        otp: str
    ) -> dict:

        if not re.fullmatch(r"\+?[0-9]{10,15}", mobile_number):
            raise ValueError("Invalid mobile number format")

        if not re.fullmatch(r"[0-9]{6}", otp):
            raise ValueError("OTP must contain exactly 6 digits")

        # Development-only mock output.
        # Never log OTPs in production.
        print("\n========== MOCK MSG91 OTP ==========")
        print("Mobile:", mobile_number)
        print("OTP:", otp)
        print("====================================\n")

        return {
            "provider": self.provider,
            "status": "simulated",
            "simulated": True,
            "delivered": False,
            "message": "Mock OTP dispatch completed successfully."
        }


msg91_service = MSG91Service()
