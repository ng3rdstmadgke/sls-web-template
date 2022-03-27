import re
import sys
from copy import deepcopy
from typing import Any, Dict, List, Tuple


def usage():
    usage = """
[ usage ]
  export $(cat .env | grep -v -e "^ *#")
  python manage.py <SUBCOMMAND> ...

[ subcommand ]
  help:
    ヘルプ表示
  show_table:
    テーブルの表示
  create_user:
    ユーザー作成
  delete_user:
    ユーザー削除
  create_role:
    ロール作成
  attach_role:
    ユーザーとロールの紐づけ
  detach_role:
    ユーザーとロールの切り離し
"""
    print(usage, file=sys.stderr)
    exit(1)

def parse(args: List[str]) -> Tuple[str, List[str], Dict[str, Any]] :
    args_copy = deepcopy(args)
    args_copy.reverse()
    if len(args_copy) < 2:
        usage()
    _ = args_copy.pop()
    subcommand = args_copy.pop()
    options = {}
    sub_args = []
    parse_inner(args_copy, sub_args, options)
    return (subcommand, sub_args, options)
        

def parse_inner(args: List[str], sub_args: List[str], options: Dict[str, Any]):
    if len(args) <= 0:
        return
    else:
        curr = args.pop()
        pat = re.compile("^--?(.*)$")
        match = pat.match(curr)
        if match: # オプション
            option = match.groups()[0]
            if (len(args) > 0 and pat.match(args[-1]) is None):
                options[option] = args.pop()
            else:
                options[option] = True
        else: # 引数
            sub_args.append(curr)
        parse_inner(args, sub_args, options)



if __name__ == "__main__":
    subcommand, args, options = parse(sys.argv)
    #print(f"SUBCOMMAND: {subcommand}, ARGS: {args}, OPTIONS: {options}", file=sys.stderr)
    #print(f"", file=sys.stderr)

    if re.match("^(-?h|-?-?help)$", subcommand):
        usage()
    elif subcommand == "show_table":
        from tools.show_table import main
        main(args, options)
    elif subcommand == "create_user":
        from tools.create_user import main
        main(args, options)
    elif subcommand == "delete_user":
        from tools.delete_user import main
        main(args, options)
    elif subcommand == "create_role":
        from tools.create_role import main
        main(args, options)
    elif subcommand == "attach_role":
        from tools.attach_role import main
        main(args, options)
    elif subcommand == "detach_role":
        from tools.detach_role import main
        main(args, options)
