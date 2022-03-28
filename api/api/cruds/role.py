from typing import Optional, List
from sqlalchemy.orm import Session

from ..models.role import Role
from ..schemas.role import RoleCreateSchema

# Session API: https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# Query API: https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query

def get_role(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.id == role_id).first()

def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    return db.query(Role).filter(Role.name == name).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
    return db.query(Role).offset(skip).limit(limit).all()

def create_role(db: Session, role_schema: RoleCreateSchema):
    role = Role(**role_schema.dict())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def update_role(db: Session, role_schema: RoleCreateSchema, role: Role) -> Role:
    role.name = role_schema.name
    role.description = role_schema.description
    db.add(role)
    db.commit()
    db.refresh(role)  # dbに登録された内容をitemに反映
    return role

def delete_role(db: Session, role: Role):
    db.delete(role)
    db.commit()
