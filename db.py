"""
Database configuration and User model.

Current database:
SQLite

Used for:
- User registration
- Password storage (hashed)
- Email verification status

Install:
pip install sqlalchemy python-dotenv
"""

import os

from dotenv import load_dotenv
from sqlalchemy import Boolean, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker
)


# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()


# =========================
# DATABASE CONFIGURATION
# =========================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./auth.db"
)


# SQLite needs check_same_thread=False
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# =========================
# BASE MODEL
# =========================

class Base(DeclarativeBase):
    pass


# =========================
# USER MODEL
# =========================

class User(Base):

    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    # User Email
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    # Hashed Password
    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # Email Verification Status
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )


# =========================
# CREATE DATABASE TABLES
# =========================

Base.metadata.create_all(
    bind=engine
)


# =========================
# DATABASE DEPENDENCY
# =========================

def get_db():
    """
    FastAPI dependency.

    Creates a database session for every request
    and automatically closes it afterwards.
    """

    db: Session = SessionLocal()

    try:
        yield db

    finally:
        db.close()