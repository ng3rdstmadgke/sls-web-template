#!/bin/bash

function usage {
cat >&2 <<EOS
テスト実行コマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
EOS
exit 1
}

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
source "${SCRIPT_DIR}/lib/utils.sh"

APP_NAME=$(get_app_name ${PROJECT_ROOT}/app_name)

ENV_PATH="${PROJECT_ROOT}/local.env"
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help     ) usage;;
    -* | --*        ) error "$1 : 不正なオプションです" ;;
    *               ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage
[ -r "$ENV_PATH" -a -f "$ENV_PATH" ] || error "環境変数ファイルが見つかりません: $ENV_PATH"

env_tmp="$(mktemp)"
cat "$ENV_PATH" > "$env_tmp"

set -e
trap 'rm $env_tmp;' EXIT

docker run --rm -ti \
  --network host \
  --env-file "$env_tmp" \
  -v "${PROJECT_ROOT}:/opt/app" \
  "${APP_NAME}/api:latest" \
  su app -c "/opt/app/bin/lib/test.sh"
