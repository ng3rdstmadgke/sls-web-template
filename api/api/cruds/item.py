from typing import Optional, List
import hashlib

from sqlalchemy.orm import Session
from sqlalchemy import or_

from api.api.env import get_env
from api.api.models.item import Item
from api.api.models.user import User
from api.api.schemas.item import (
    DataFormat,
)

def get_item_name(file_id: int) -> str:
    env = get_env()
    return "{}-{}-{:0>8}".format(
        env.app_name,
        env.stage_name,
        file_id,
    )

def get_for_translate(db: Session, user_id: int, item_id: int) -> Optional[Item]:
    return db \
        .query(
            Item.id,
            Item.name,
            Item.user_id,
        ) \
        .filter(
            or_(
                Item.user_id == user_id,
                Item.is_common == True,
            ),
            Item.id == item_id
        ) \
        .first()


def get(db: Session, user_id: int, item_id: int) -> Optional[Item]:
    return db.query(Item) \
        .filter(
            Item.user_id == user_id,
            Item.id == item_id,
        ) \
        .first()

def get_include_common(db: Session, user_id: int, item_id: int) -> Optional[Item]:
    return db.query(
            Item.id,
            Item.name,
            Item.content,
            Item.is_common,
            Item.data_format,
            (Item.user_id == user_id).label("owner"),
        ) \
        .filter(
            or_(
                Item.user_id == user_id,
                Item.is_common == True,
            ),
            Item.id == item_id
        ) \
        .first()

def get_list_include_common(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(
            Item.id,
            Item.name,
            Item.is_common,
            Item.data_format,
            (Item.user_id == user_id).label("owner"),
        ) \
        .filter(
            or_(
                Item.user_id == user_id,
                Item.is_common == True,
            )
        ) \
        .offset(skip) \
        .limit(limit) \
        .all()

def create(
    db: Session,
    name: str,
    content: str,
    is_common: bool,
    data_format: DataFormat,
    user: User
) -> Item:
    item = Item(
        name=name,
        content=content,
        is_common=is_common,
        data_format=data_format,
    )
    user.items.append(item)
    db.add(user)
    db.commit()
    db.refresh(item)
    return item

def update(
    db: Session,
    name: str,
    content: str,
    is_common: bool,
    data_format: DataFormat,
    item: Item,
) -> Item:
    item.name = name
    item.content = content
    item.is_common = is_common
    item.data_format = data_format
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete(db: Session, item: Item):
    db.delete(item)
    db.commit()