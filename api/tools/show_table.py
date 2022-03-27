from pprint import pprint
import sys
from typing import Any, Dict, List
from sqlalchemy.sql import text
from sqlalchemy import select
from pydantic import BaseModel

from api.db.db import SessionLocal


class Args(BaseModel):
    table_name: str

class Options(BaseModel):
    limit: int = 100
    offset: int = 0 

def usage():
    usage = """
テーブルを表示する

[ usage ]
  python manage.py show_table --list
  python manage.py show_table <TABLE_NAME> [OPTIONS]

[ args ]
  TABLE_NAME:
    テーブル名

[ options ]
  --limit <INT>:
    select件数
  --offset <INT>:
    select開始オフセット
  -h | --help:
    ヘルプ
"""
    print(usage, file=sys.stderr)
    exit(1)

def result_dict(r):
    return dict(zip(r.keys(), map(lambda e: str(e), r)))

def print_table_format(rows):
    for (i, row) in enumerate(rows):
        if (i == 0):
            print("\t".join(result_dict(row).keys()))
        print("\t".join(result_dict(row).values()))


def main(args: List[str], options: Dict[str, Any]):
    if ("list" in options):
        with SessionLocal() as db:
            rows = db.execute(text("SHOW TABLES"))
            print_table_format(rows)
        exit(0)
        
    if (len(args) != 1):
        usage()
    
    if ("h" in options or "help" in options):
        usage()

    arg_obj = Args.parse_obj({"table_name": args[0]})
    option_obj = Options.parse_obj(options)
    with SessionLocal() as db:
        stmt = text(f"SELECT * FROM `{arg_obj.table_name}` LIMIT :limit OFFSET :offset")
        bind = {
          "limit": int(option_obj.limit),
          "offset": int(option_obj.offset),
        }
        rows = db.execute(stmt, bind)
    print_table_format(rows)