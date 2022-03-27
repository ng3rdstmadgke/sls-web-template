import sys
from typing import Any, Dict, List
from api.db.db import SessionLocal
from api.db.base import User
from pydantic import BaseModel

class Args(BaseModel):
    user_name: str

class Options(BaseModel):
    physical: bool = False

def usage():
    usage = """
ユーザーを削除する(デフォルトは論理削除)

[ usage ]
  python manage.py delete_user <USER_NAME> [OPTIONS]

[ args ]
  USER_NAME:
    ユーザー名

[ options ]
  --physical:
    物理削除を行う
  -h | --help:
    ヘルプ
"""
    print(usage, file=sys.stderr)
    exit(1)

def main(args: List[str], options: Dict[str, Any]):
    if (len(args) != 1):
        usage()
    
    if ("h" in options or "help" in options):
        usage()

    arg_obj = Args.parse_obj({"user_name": args[0]})
    option_obj = Options.parse_obj(options)
    with SessionLocal() as db:

        user = db.query(User).filter(User.username == arg_obj.user_name).first()
        if user is None:
            raise Exception(f"ユーザー({arg_obj.user_name}) が見つかりません。")

        if option_obj.physical:
            db.delete(user)
            db.commit()
        else:
            user.is_active = False
            db.add(user)
            db.commit()
            db.refresh(user)
