from typing import List
from pydantic import BaseModel

from api.api.schemas.role import RoleSchema
from api.api.schemas.item import ItemSchema

class UserSchemaBase(BaseModel):
    """Userの参照・作成で共通して必要になるメンバを定義したスキーマ"""
    username: str

class UserCreateSchema(UserSchemaBase):
    """User作成時に利用されるスキーマ"""
    password: str

class UserUpdateSchema(UserSchemaBase):
    is_superuser: bool
    is_active: bool

class UserSchema(UserSchemaBase):
    """Userの参照時や、APIからの返却データとして利用されるスキーマ"""
    id: int
    is_superuser: bool
    is_active: bool
    roles: List[RoleSchema] = []
    # NOTE: 重くなるし使わないのでひとまず出力しない
    #items: List[ItemSchema]
    
    class Config:
        orm_mode = True