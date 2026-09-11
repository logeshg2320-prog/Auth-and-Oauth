"""
JWT authentication + password hashing utilities.

Used by:
- main.py
- SQLite user authentication
- JWT protected routes

Install:
pip install pyjwt "pwdlib[argon2]" python-multipart python-dotenv
"""

import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash


# Load environment variables from .env
load_dotenv()


# =========================
# JWT CONFIGURATION
# =========================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is missing from .env file"
    )

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =========================
# PASSWORD HASHING
# =========================

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a user's password before storing it in the database."""

    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """Verify login password against stored hashed password."""

    return password_hash.verify(
        plain_password,
        hashed_password
    )


# =========================
# JWT TOKEN
# =========================

# tokenUrl should match your login endpoint
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def create_access_token(
    data: dict,
    expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    """Create JWT access token."""

    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=expires_minutes)
    )

    to_encode["exp"] = expire

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================
# CURRENT USER
# =========================

def get_current_user_email(
    token: str = Depends(oauth2_scheme)
) -> str:
    """
    Extract and verify email from JWT token.

    Used for protected routes.
    """

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_error

        return email

    except InvalidTokenError:
        raise credentials_error