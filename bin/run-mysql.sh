#!/bin/bash
shopt -s expand_aliases
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc

function usage {
cat >&2 <<EOS
mysqlコンテナ起動コマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -d | --daemon:
   バックグラウンドで起動
EOS
exit 1
}

SCRIPT_DIR="$(cd $(dirname $0); pwd)"
PROJECT_ROOT="$(cd ${SCRIPT_DIR}/..; pwd)"
API_DIR="$(cd ${PROJECT_ROOT}/api; pwd)"
CONTAINER_DIR="$(cd ${PROJECT_ROOT}/docker; pwd)"
BIN_DIR="$(cd ${PROJECT_ROOT}/bin; pwd)"

source "${SCRIPT_DIR}/lib/utils.sh"

APP_NAME=$(get_app_name ${PROJECT_ROOT}/app_name)

OPTIONS=
DAEMON=
ENV_PATH="${PROJECT_ROOT}/local.env"
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help   ) usage;;
    -d | --daemon ) shift;DAEMON=1;OPTIONS="$OPTIONS -d";;
    -* | --*      ) error "$1 : 不正なオプションです" ;;
    *             ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage
[ -r "$ENV_PATH" -a -f "$ENV_PATH" ] || error "環境変数ファイルが見つかりません: $ENV_PATH"


env_tmp="$(mktemp)"
cat "$ENV_PATH" > "$env_tmp"

set -e
trap 'rm $env_tmp' EXIT
export $(cat $env_tmp | grep -v -e "^ *#.*")

cd "$CONTAINER_DIR"
invoke docker run $OPTIONS \
  --rm \
  --name ${APP_NAME}-mysql \
  --network host \
  -e MYSQL_ROOT_PASSWORD=$DB_PASSWORD \
  -e MYSQL_USER=$DB_USER \
  -e MYSQL_PASSWORD=$DB_PASSWORD \
  -e MYSQL_DATABASE=$DB_NAME \
  "${APP_NAME}/mysql:latest"

if [ -n "$DAEMON" ]; then
  invoke docker run \
    --rm \
    --name ${APP_NAME}-mysql-check \
    --env-file "$env_tmp" \
    --network host \
    -v "${PROJECT_ROOT}:/opt/app" \
    "${APP_NAME}/api:latest" \
    /opt/app/bin/lib/check-mysql-boot.sh
fi