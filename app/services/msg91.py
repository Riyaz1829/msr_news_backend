
import os

from dotenv import load_dotenv

load_dotenv()


class MSG91Service:
    def __init__(self):
        self.auth_key = os.getenv("MSG91_AUTH_KEY")
        self.template_id = os.getenv("MSG91_TEMPLATE_ID")
        self.sender_id = os.getenv("MSG91_SENDER_ID")
        self.entity_id = os.getenv("MSG91_ENTITY_ID")

    async def send_otp(self, mobile_number: str, otp: str):
        # Do not send real SMS until MSG91 credentials
        # and approved DLT configuration are available.

        if not all([
            self.auth_key,
            self.template_id,
            self.sender_id,
            self.entity_id,
        ]):
            return {
                "provider": "mock",
                "status": "simulated",
                "delivered": False,
                "message": "MSG91 credentials are not configured.",
            }

        # Real MSG91 API integration will be added
        # after confirming the approved API endpoint
        # and request format for your account.
        raise NotImplementedError(
            "Real MSG91 integration is not configured yet."
        )


msg91_service = MSG91Service()
