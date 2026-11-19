from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):

    __tablename__ = "users"

    # Unique User ID
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    # User Full Name
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Mobile Number
    mobile_number: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False
    )

    # Email Address
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    # Hashed Password
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )