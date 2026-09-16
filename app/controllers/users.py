from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.dependencies.auth import get_password_hash


def create_user(db: Session, user_data: UserCreate):
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        return None

    hashed_password = get_password_hash(user_data.password)

    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = get_user(db, user_id)

    if not user:
        return None

    data = user_data.model_dump(exclude_unset=True)

    if "password" in data:
        data["password"] = get_password_hash(data["password"])

    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)

    if not user:
        return None

    db.delete(user)
    db.commit()

    return user