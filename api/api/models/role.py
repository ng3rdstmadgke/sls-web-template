from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

from api.api.db.base_class import Base

class UserRole(Base):
    """usersテーブルとrolesテーブルの中間テーブル"""
    __tablename__ = "user_roles"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255, collation="utf8mb4_bin"), unique=True, index=True, nullable=False)
    description = Column(String(255))
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    users = relationship("User", secondary="user_roles", back_populates="roles")