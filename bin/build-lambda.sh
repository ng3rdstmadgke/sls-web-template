#!/bin/bash
shopt -s expand_aliases
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc

function usage {
cat >&2 <<EOS
dockerイメージビルドコマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -s | --stage <STAGE_NAME>: (required)
 --no-cache:
   キャッシュを使わないでビルド
 --proxy:
   プロキシ設定を有効化
EOS
exit 1
}

proxy="http://xxxxxxx.jp:7080"
no_proxy="169.254.169.254,169.254.170.2"

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
source "${SCRIPT_DIR}/lib/utils.sh"

APP_NAME=$(get_app_name ${PROJECT_ROOT}/app_name)

TAG=latest
OPTIONS=
STAGE=
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help  ) usage;;
    -s | --stage ) shift;STAGE="$1";;
    --no-cache   ) OPTIONS="$OPTIONS --no-cache";;
    --proxy      ) OPTIONS="$OPTIONS --build-arg proxy=$proxy --build-arg no_proxy=$no_proxy";;
    -* | --*     ) error "$1 : 不正なオプションです" ;;
    *            ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage
[ -z "${STAGE}" ] && error "-s | --stage オプションを指定してください"

cd "$PROJECT_ROOT"
set -e
invoke docker build $OPTIONS \
  --rm \
  --build-arg api_gateway_base_path=/${STAGE} \
  -f docker/lambda/Dockerfile \
  -t "${APP_NAME}/lambda:${TAG}" .