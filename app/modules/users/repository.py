
from sqlalchemy.orm import Session

from app.modules.users.models import User


# Get user by email
def get_user_by_email(db: Session, email: str):

    return db.query(User).filter(
        User.email == email
    ).first()


# Get user by mobile number
def get_user_by_mobile(db: Session, mobile_number: str):

    return db.query(User).filter(
        User.mobile_number == mobile_number
    ).first()


# Get user by ID
def get_user_by_id(db: Session, user_id: int):

    return db.query(User).filter(
        User.id == user_id
    ).first()


# Create new user
def create_user(db: Session, user_data: dict):

    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
