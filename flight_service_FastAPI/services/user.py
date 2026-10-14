
from fastapi import HTTPException

from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate):
    db_user = User(
        name=user_data.name,
        email=user_data.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def all_users(db: Session):
    users = db.query(User).all()
    return users


def user_by_id(db: Session, userId: int):

    user = db.query(User).filter(User.id == userId).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user



def update_user(db: Session, userId: int, updated_user: UserCreate):
    user = db.query(User).filter(User.id == userId).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = updated_user.name
    user.email = updated_user.email

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, userId: int):
    user = db.query(User).filter(User.id == userId).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


