from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.password is not None:
        user.hashed_password = get_password_hash(user_in.password)
    db.commit()
    db.refresh(user)
    return user