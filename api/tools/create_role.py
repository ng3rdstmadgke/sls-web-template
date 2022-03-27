import sys
from typing import Any, Dict, List
from api.db.db import SessionLocal
from api.db.base import Role
from pydantic import BaseModel

class Args(BaseModel):
    role_name: str

class Options(BaseModel):
    desc: str = ""

def usage():
    usage = """
ロールを作成する

[ usage ]
  python manage.py create_role <ROLE_NAME> [OPTIONS]

[ args ]
  ROLE_NAME:
    ロール名

[ options ]
  --desc <STR>:
    ロールの説明
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

    arg_obj = Args.parse_obj({"role_name": args[0]})
    option_obj = Options.parse_obj(options)
    with SessionLocal() as db:
        role = db.query(Role).filter(Role.name == arg_obj.role_name).first()
        if role is not None:
            raise Exception(f"{arg_obj.role_name} は既に存在しています。")
        role = Role(
            name=arg_obj.role_name,
            description=option_obj.desc
        )
        db.add(role)
        db.commit()
        db.refresh(role)
