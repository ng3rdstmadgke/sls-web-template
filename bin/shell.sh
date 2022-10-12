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
 --profile <AWS_PROFILE>:
   awsのプロファイル名を指定 (default=default)
 --region <AWS_REGION>:
   awsのリージョンを指定 (default=ap-northeast-1)
EOS
exit 1
}

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
source "${SCRIPT_DIR}/lib/utils.sh"

APP_NAME=$(get_app_name ${PROJECT_ROOT}/app_name)

AWS_PROFILE="default"
AWS_REGION="ap-northeast-1"
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help     ) usage;;
    -e | --env-file ) shift;ENV_PATH="$1";;
    --profile       ) shift;AWS_PROFILE="$1";;
    --region        ) shift;AWS_REGION="$1";;
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

AWS_ACCESS_KEY_ID=$(aws --profile $AWS_PROFILE --region $AWS_REGION configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws --profile $AWS_PROFILE --region $AWS_REGION configure get aws_secret_access_key)
echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> "$env_tmp"
echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> "$env_tmp"

set -e
trap 'rm $env_tmp;' EXIT
cat $env_tmp
docker run --rm -ti \
  --network host \
  --env-file "$env_tmp" \
  -e LOCAL_UID=$(id -u) \
  -e LOCAL_GID=$(id -g) \
  -v "${PROJECT_ROOT}:/opt/app" \
  "${APP_NAME}/api:latest" \
  /usr/local/bin/shell-entrypoint.sh