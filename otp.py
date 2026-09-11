import os
import secrets
import smtplib
from email.message import EmailMessage

import redis
from dotenv import load_dotenv

load_dotenv()


r = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True
)

OTP_EXPIRE_SECONDS = 5 * 60


def _key(email: str, purpose: str) -> str:
    return f"otp:{purpose}:{email.lower()}"


def generate_otp(email: str, purpose: str = "verification") -> str:
    otp = f"{secrets.randbelow(1_000_000):06d}"

    r.setex(
        _key(email, purpose),
        OTP_EXPIRE_SECONDS,
        otp
    )

    return otp


def verify_otp(
    email: str,
    submitted_otp: str,
    purpose: str = "verification"
) -> bool:

    stored = r.get(_key(email, purpose))

    if stored is None:
        return False

    if not secrets.compare_digest(stored, submitted_otp):
        return False

    # Delete OTP after successful verification
    r.delete(_key(email, purpose))

    return True


def send_otp_email(
    email: str,
    otp: str,
    purpose: str = "verification"
) -> None:

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        raise RuntimeError(
            "EMAIL_ADDRESS or EMAIL_PASSWORD is missing in .env file"
        )

    # Different email based on purpose
    if purpose == "password_reset":
        subject = "Reset Your Password"
        message_body = f"""
Hello,

We received a request to reset the password for your account.

Your password reset verification code is:

{otp}

This code will expire in 5 minutes.

For your security:

• Never share this code with anyone.
• Our support team will never ask for your OTP.
• If you did not request a password reset, please ignore this email.

Thanks,
Authentication System Security Team
"""
    else:
        subject = "Verify Your Email Address"
        message_body = f"""
Hello,

Thank you for signing up.

Your email verification code is:

{otp}

This code will expire in 5 minutes.

Please do not share this code with anyone.

Thanks,
Authentication System
"""

    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = email

    message.set_content(message_body)

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            sender_email,
            sender_password
        )

        smtp.send_message(message)

    print(f"OTP sent successfully to {email}")