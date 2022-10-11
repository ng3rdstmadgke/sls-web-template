#!/bin/bash

function usage {
cat >&2 <<EOS
DBログインコマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -e | --env-file <ENV_PATH>: (required)
   環境変数ファイルを指定
EOS
exit 1
}

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
source "${SCRIPT_DIR}/lib/utils.sh"

APP_NAME=$(get_app_name ${PROJECT_ROOT}/app_name)

args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help     ) usage;;
    -e | --env-file ) shift;ENV_PATH="$1";;
    -* | --*        ) error "$1 : 不正なオプションです" ;;
    *               ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage
[ -z "$ENV_PATH" ] && error "-e | --env でコンテナ用の環境変数ファイルを指定してください"
[ -r "$ENV_PATH" -a -f "$ENV_PATH" ] || error "コンテナ用の環境変数ファイルを読み込めません: $ENV_PATH"

env_tmp="$(mktemp)"
cat "$ENV_PATH" > "$env_tmp"

set -e
trap 'rm $env_tmp;' EXIT

docker run --rm -ti \
  --network host \
  --env-file "$env_tmp" \
  -e LOCAL_UID=$(id -u) \
  -e LOCAL_GID=$(id -g) \
  -v "${PROJECT_ROOT}:/opt/app" \
  "${APP_NAME}/api:latest" \
  /usr/local/bin/shell-entrypoint.sh