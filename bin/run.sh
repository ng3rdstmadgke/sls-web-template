#!/bin/bash
shopt -s expand_aliases
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc

function usage {
cat >&2 <<EOS
コンテナ起動コマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -d | --daemon:
   バックグラウンドで起動
 -e | --env-file <ENV_PATH>:
   apiコンテナ用の環境変数ファイルを指定(default=.env)
 --debug:
   デバッグモードで起動
EOS
exit 1
}

SCRIPT_DIR="$(cd $(dirname $0); pwd)"
PROJECT_ROOT="$(cd ${SCRIPT_DIR}/..; pwd)"
API_DIR="$(cd ${PROJECT_ROOT}/api; pwd)"
FRONT_DIR="$(cd ${PROJECT_ROOT}/front; pwd)"
CONTAINER_DIR="$(cd ${PROJECT_ROOT}/docker; pwd)"
DEBUG=

source "${SCRIPT_DIR}/lib/utils.sh"

OPTIONS=
ENV_PATH="${PROJECT_ROOT}/.env"
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help      ) usage;;
    -d | --daemon    ) shift;OPTIONS="$OPTIONS -d";;
    -e | --env-file  ) shift;ENV_PATH="$1";;
    --debug          ) DEBUG="1";;
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

trap "docker-compose -f docker-compose.yml down; rm $api_env_tmp $front_env_tmp" EXIT
invoke export API_DIR="$API_DIR"
invoke export FRONT_DIR="$FRONT_DIR"
invoke export ENV_PATH="$api_env_tmp"
invoke export APP_NAME=$(get_app_name ${PROJECT_ROOT}/app_name)
invoke export API_GATEWAY_ROOT_PATH="/dev/"
cd "$CONTAINER_DIR"

cat $ENV_PATH
if [ -n "$DEBUG" ]; then
  invoke docker-compose -f docker-compose-dev.yml down
  invoke docker-compose -f docker-compose-dev.yml up $OPTIONS
else
  invoke docker-compose -f docker-compose.yml down
  invoke docker-compose -f docker-compose.yml up $OPTIONS
fi