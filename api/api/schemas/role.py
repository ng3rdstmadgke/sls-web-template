from typing import Optional
from pydantic import BaseModel

class RoleSchemaBase(BaseModel):
    """Roleの参照・作成で共通して必要になるメンバを定義したスキーマ"""
    name: str
    description: Optional[str] = None

class RoleCreateSchema(RoleSchemaBase):
    """Role作成時に利用されるスキーマ"""
    pass

class RoleSchema(RoleSchemaBase):
    """Roleの参照時や、APIからの返却データとして利用されるスキーマ"""
    id: int
    
    class Config:
        orm_mode = True
