from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException

from api.api import auth
from api.api.db import db
from api.api.models.user import User
from api.api.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema
from api.api.cruds import (
    user as crud_user,
    role as crud_role,
) 

router = APIRouter()

@router.get("/users/me", response_model=UserSchema)
def read_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user

# Depends(Callable[..., Any]) は引数に取った関数を実行してその実行結果を返す。
#  Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
@router.post("/users/", response_model=UserSchema)
def create_user(
    user_schema: UserCreateSchema,
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    user = crud_user.get_user_by_name(db, username=user_schema.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registerd")
    return crud_user.create_user(db, user_schema)

@router.get("/users/", response_model=List[UserSchema])
def read_users(
    skip: int = 0, # GETパラメータ
    limit: int = 100, # GETパラメータ
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    users = crud_user.get_users(db, skip=skip, limit = limit)
    return users

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int, # URLの{user_id}プレースホルダ
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    user = crud_user.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#@router.put("/users/{user_id}/password", response_model=UserSchema)
#def update_user_password(
#    user_id: int,
#    user_schema: UserCreateSchema,
#    db: Session = Depends(db.get_db),
#    _: User = Depends(auth.get_current_admin_user)
#):
#    user = crud_user.get_user(db, user_id=user_id)
#    if user is None:
#        raise HTTPException(status_code=404, detail="User not found")
#    return crud_user.update_user_password(db, user_schema, user)

@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_schema: UserUpdateSchema,
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    user = crud_user.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update_user(db, user_schema, user)

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    user = crud_user.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.delete_user(db, user)
    return {"user_id": user_id}

@router.post("/users/{user_id}/roles/{role_id}", response_model=UserSchema)
def associate_user_role(
    user_id: int,
    role_id: int,
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    """userとroleを関連付ける

    Args:
        user_id (int): roleを関連付けるユーザーのid
        role_id (int): userに関連付けるロールのid
        db (Session, optional): セッション
        _ (User, optional): アドミンユーザー認証

    Raises:
        HTTPException: user_id, role_idで指定したリソースが見つからない場合の例外
    """
    user = crud_user.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    role = crud_role.get_role(db, role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return crud_user.append_role(db, user, role)