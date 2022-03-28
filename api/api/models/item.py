from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.sql.sqltypes import DateTime, Enum

from ..db.base_class import Base
from ..schemas.item import DataFormat

class Item(Base):
    __tablename__ = "items"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255, collation="utf8mb4_bin"), nullable=False, index=True)
    content = Column(MEDIUMTEXT)
    is_common = Column(Boolean, default=False, nullable=False)
    data_format = Column(Enum(DataFormat), nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # リレーション
    user = relationship("User", back_populates="items")