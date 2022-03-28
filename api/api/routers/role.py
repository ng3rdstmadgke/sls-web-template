
from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status

from .. import auth
from ..db import db
from ..models.user import User
from ..schemas.role import RoleSchema, RoleCreateSchema
from ..cruds import (
    role as crud_role,
) 

router = APIRouter()

@router.post("/roles/", response_model=RoleSchema)
def create_role(
    role_schema: RoleCreateSchema,
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    role = crud_role.get_role_by_name(db, role_schema.name)
    if role:
        raise HTTPException(status_code=400, detail="Role already registerd")
    return crud_role.create_role(db=db, role_schema=role_schema)

@router.get("/roles/", response_model=List[RoleSchema])
def read_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    roles = crud_role.get_roles(db, skip=skip, limit = limit)
    return roles

@router.get("/roles/{role_id}", response_model=RoleSchema)
def read_role(
    role_id: int,
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    role = crud_role.get_role(db, role_id=role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/roles/{role_id}", response_model=RoleSchema)
def update_role(
    role_id: int,
    role_schema: RoleCreateSchema,
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    role = crud_role.get_role(db, role_id=role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return crud_role.update_role(db, role_schema, role)

@router.delete("/roles/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(db.get_db),
    _: User = Depends(auth.get_current_admin_user)
):
    role = crud_role.get_role(db, role_id=role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    crud_role.delete_role(db, role)
    return {"role_id": role_id}