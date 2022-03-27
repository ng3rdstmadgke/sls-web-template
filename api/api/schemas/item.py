from typing import Optional
from pydantic import BaseModel
import enum


class DataFormat(str, enum.Enum):
    CSV = "CSV",
    TSV = "TSV"

class ItemSchemaBase(BaseModel):
    id: int
    name: str
    is_common: bool
    data_format: DataFormat

class ItemSchema(ItemSchemaBase):
    content: str
    owner: bool = True  # 自身で作成した辞書ファイルかどうか
    class Config:  # innerクラス Config にはpydanticの設定を定義する
        # dictではなくORMオブジェクトを渡された場合でもデータを読み込むようにする
        # id = data["id"] で読み込めなかった場合に id = data.id でリトライする
        # 例えばuser.itemsのようにリレーションで遅延評価されるプロパティでも利用できる
        orm_mode = True

class ItemSchemaWithoutContent(ItemSchemaBase):
    owner: bool = True  # 自身で作成した辞書ファイルかどうか
    class Config:
        orm_mode = True