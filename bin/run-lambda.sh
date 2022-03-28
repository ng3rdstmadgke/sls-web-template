#!/bin/bash -l

function usage {
cat >&2 <<EOS
lambdaコンテナ起動コマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -d | --daemon:
   バックグラウンドで起動
 -e | --env-file <ENV_PATH>:
   apiコンテナ用の環境変数ファイルを指定(default=.env)
EOS
exit 1
}

SCRIPT_DIR="$(cd $(dirname $0); pwd)"
PROJECT_ROOT="$(cd ${SCRIPT_DIR}/..; pwd)"
source "${SCRIPT_DIR}/lib/utils.sh"

APP_NAME=$(get_app_name ${PROJECT_ROOT}/app_name)

OPTIONS=
ENV_PATH=
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help      ) usage;;
    -d | --daemon    ) shift;OPTIONS="$OPTIONS -d";;
    -e | --env-file  ) shift;ENV_PATH="$1";;
    -* | --*         ) error "$1 : 不正なオプションです" ;;
    *                ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage
[ -z "$ENV_PATH" ] && error "-e | --env-file で環境変数ファイルを指定してください"
[ -r "$ENV_PATH" -a -f "$ENV_PATH" ] || error "指定した環境変数ファイルを読み込めません: $ENV_PATH"

api_env_tmp="$(mktemp)"
cat "$ENV_PATH" > "$api_env_tmp"


invoke cat $ENV_PATH
invoke docker run $OPTIONS \
  --rm \
  --name ${APP_NAME}-lambda \
  --env-file "$ENV_PATH" \
  -p 8080:8080 \
  "${APP_NAME}/lambda:latest"