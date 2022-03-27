from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from api.db.base_class import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255, collation="utf8mb4_bin"), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # カスケード: https://docs.sqlalchemy.org/en/14/orm/cascades.html
    # 一対多のリレーション: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    items = relationship(
        "Item",                      # リレーション先のモデルクラス名
        back_populates="user",       # リレーション先の変数名
        cascade="all, delete-orphan" # Userレコードを削除したとに関連するitemsを削除する(default="save-update")
    )

    # 多対多のリレーション: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
    roles = relationship(
        "Role",
        secondary="user_roles", # 中間テーブルを指定
        back_populates="users"
    )