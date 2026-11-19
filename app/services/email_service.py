
class EmailService:

    def __init__(self):
        self.provider = "mock"

    async def send_password_reset_email(
        self,
        recipient_email: str,
        reset_link: str
    ) -> dict:

        # Simulate email delivery
        print("\n========== MOCK PASSWORD RESET EMAIL ==========")
        print("To:", recipient_email)
        print("Reset Link:", reset_link)
        print("================================================\n")

        return {
            "provider": self.provider,
            "status": "simulated",
            "delivered": False,
            "message": "Mock password reset email generated."
        }


email_service = EmailService()
