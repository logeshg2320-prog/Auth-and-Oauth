"""
Authentication API

Flow:
Signup
    ↓
Store user in database
    ↓
Generate OTP in Redis
    ↓
Send OTP through Gmail
    ↓
Verify Email
    ↓
Login
    ↓
Generate JWT
"""

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from auth import (
    create_access_token,
    get_current_user_email,
    hash_password,
    verify_password
)

from db import User, get_db

from otp import (
    generate_otp,
    send_otp_email,
    verify_otp
)

import os

from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware

from google_auth import oauth



# =========================
# FASTAPI APP
# =========================

app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# =========================
# REQUEST MODELS
# =========================

class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class OTPRequest(BaseModel):
    email: EmailStr
    otp: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
    confirm_password: str

# =========================
# SIGNUP
# =========================

@app.post("/signup")
def signup(
    body: SignupRequest,
    db: Session = Depends(get_db)
):

    # Check if user already exists
    existing_user = db.query(User).filter(
        User.email == body.email
    ).first()

    # -----------------------------------
    # USER ALREADY EXISTS
    # -----------------------------------

    if existing_user:

        # If email is already verified
        if existing_user.is_verified:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered. Please login."
            )

        # User exists but email is NOT verified
        # Generate a new OTP and resend it

        otp = generate_otp(body.email)

        send_otp_email(
            email=body.email,
            otp=otp
        )

        return {
            "message": "Account exists but email is not verified. A new OTP has been sent."
        }


    # -----------------------------------
    # NEW USER
    # -----------------------------------

    user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        is_verified=False
    )

    db.add(user)
    db.commit()


    # Generate OTP
    otp = generate_otp(body.email)


    # Send OTP to user's email
    send_otp_email(
        email=body.email,
        otp=otp
    )


    return {
        "message": "Account created successfully. Check your email for the OTP."
    }


# =========================
# VERIFY EMAIL OTP
# =========================

@app.post("/verify-email")
def verify_email(
    body: OTPRequest,
    db: Session = Depends(get_db)
):

    # Verify OTP from Redis
    if not verify_otp(
        body.email,
        body.otp
    ):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )


    # Find user
    user = db.query(User).filter(
        User.email == body.email
    ).first()


    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


    # Mark user as verified
    user.is_verified = True

    db.commit()


    return {
        "message": "Email verified successfully. You can now login."
    }


# =========================
# LOGIN
# =========================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Find user
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()


    # Check email and password
    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    # Check if email is verified
    if not user.is_verified:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email first"
        )


    # Create JWT token
    token = create_access_token(
        {
            "sub": user.email
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ==================================
# GOOGLE LOGIN - REDIRECT TO GOOGLE
# ==================================

@app.get("/login/google")
async def login_google(request: Request):

    redirect_uri = "http://localhost:8000/auth/google"

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )


# ==================================
# GOOGLE CALLBACK
# ==================================

@app.get("/auth/google")
async def auth_google(
    request: Request,
    db: Session = Depends(get_db)
):

    token = await oauth.google.authorize_access_token(request)

    user_info = token.get("userinfo")

    if not user_info:
        raise HTTPException(
            status_code=400,
            detail="Could not retrieve Google user information"
        )

    email = user_info.get("email")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Google account does not provide an email"
        )

    # Check whether user already exists
    user = db.query(User).filter(
        User.email == email
    ).first()

    # Create Google user if they don't exist
    if not user:

        user = User(
            email=email,
            hashed_password=hash_password(os.urandom(32).hex()),
            is_verified=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    # Create JWT token for YOUR application
    access_token = create_access_token(
        {"sub": email}
    )

    return RedirectResponse(
        url=f"http://localhost:5173/auth/google/callback?access_token={access_token}"
    )

# =========================
# PROTECTED ROUTE
# =========================

@app.post("/forgot-password")
def forgot_password(
    body: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == body.email)
        .first()
    )

    # Security:
    # Don't reveal whether an email exists or not
    if not user:
        return {
            "message":
            "If an account exists with this email, "
            "a password reset code has been sent."
        }

    otp = generate_otp(
        body.email,
        purpose="password_reset"
    )

    send_otp_email(
        body.email,
        otp,
        purpose="password_reset"
    )

    return {
        "message":
        "If an account exists with this email, "
        "a password reset code has been sent."
    }

@app.post("/reset-password")
def reset_password(
    body: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    # Check passwords match
    if body.new_password != body.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Verify OTP
    valid = verify_otp(
        body.email,
        body.otp,
        purpose="password_reset"
    )

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )

    user = (
        db.query(User)
        .filter(User.email == body.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Save NEW password (not confirm_password)
    user.hashed_password = hash_password(
        body.new_password
    )

    db.commit()

    return {
        "message": "Password reset successfully"
    }


@app.get("/me")
def read_me(
    email: str = Depends(get_current_user_email)
):

    return {
        "email": email
    }