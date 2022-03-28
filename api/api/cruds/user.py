from typing import Optional
from sqlalchemy.orm import Session

from .. import auth
from ..models.user import User
from ..models.role import Role
from ..schemas.user import UserCreateSchema, UserUpdateSchema

# Session API: https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# Query API: https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_name(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user_schema: UserCreateSchema) -> User:
    hashed_password = auth.get_password_hash(user_schema.password)
    user = User(
        username=user_schema.username,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_user_if_not_exists(db: Session, user_schema: UserCreateSchema) -> User:
    user = db.query(User).filter(User.username == user_schema.username).first()
    if user is not None:
        return user
    hashed_password = auth.get_password_hash(user_schema.password)
    user = User(
        username=user_schema.username,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_password(db: Session, user_schema: UserCreateSchema, user: User) -> User:
    user.username = user_schema.username
    user.hashed_password = auth.get_password_hash(user_schema.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_schema: UserUpdateSchema, user: User) -> User:
    user.username = user_schema.username
    user.is_superuser = user_schema.is_superuser
    user.is_active = user_schema.is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()

def append_role(db: Session, user: User, role: Role) -> User:
    user.roles.append(role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    