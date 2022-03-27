import sys
from typing import Any, Dict, List
from api import auth
from api.db.db import SessionLocal
from api.db.base import User
from pydantic import BaseModel

class Args(BaseModel):
    user_name: str

class Options(BaseModel):
    superuser: bool = False

def usage():
    usage = """
ユーザーを作成する

[ usage ]
  python manage.py create_user <USER_NAME> [OPTIONS]

[ args ]
  USER_NAME:
    ユーザー名

[ options ]
  --superuser:
    管理ユーザーを作成するオプション
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

    print("password: ", end="")
    password = input().strip()
    print("password: ", end="")
    confirmation = input().strip()

    if password != confirmation:
        raise Exception("パスワードが一致しません")

    with SessionLocal() as db:
        user = db.query(User).filter(User.username == arg_obj.user_name).first()
        if user is not None:
            raise Exception(f"{arg_obj.user_name} は既に存在しています。")
        hashed_password = auth.get_password_hash(password)
        db_user = User(
            username=arg_obj.user_name,
            hashed_password=hashed_password,
            is_superuser=option_obj.superuser,
            is_active=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)