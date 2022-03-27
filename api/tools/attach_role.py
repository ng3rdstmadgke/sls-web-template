import sys
from typing import Any, Dict, List
from api.db.db import SessionLocal
from api.db.base import Role
from api.db.base import User
from pydantic import BaseModel

class Args(BaseModel):
    user_name: str
    role_name: str

class Options(BaseModel):
    pass

def usage():
    usage = """
ユーザーにロールを紐づける

[ usage ]
  python manage.py attach_role <USER_NAME> <ROLE_NAME> [OPTIONS]

[ args ]
  USER_NAME:
    ユーザー名
  ROLE_NAME:
    ロール名

[ options ]
  -h | --help:
    ヘルプ
"""
    print(usage, file=sys.stderr)
    exit(1)

def main(args: List[str], options: Dict[str, Any]):
    if (len(args) != 2):
        usage()
    
    if ("h" in options or "help" in options):
        usage()

    arg_obj = Args.parse_obj({"user_name": args[0], "role_name": args[1]})
    option_obj = Options.parse_obj(options)
    with SessionLocal() as db:

        user = db.query(User).filter(User.username == arg_obj.user_name).first()
        if user is None:
            raise Exception(f"ユーザー({arg_obj.user_name}) が見つかりません。")

        role = db.query(Role).filter(Role.name == arg_obj.role_name).first()
        if role is None:
            raise Exception(f"ロール({arg_obj.role_name}) が見つかりません")

        user.roles.append(role)
        db.add(user)
        db.commit()
        db.refresh(user)
