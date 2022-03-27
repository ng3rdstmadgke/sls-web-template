#!/bin/bash
function usage {
cat >&2 <<EOS
デプロイコマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -s | --stage <STAGE_NAME>: (required)
   デプロイステージを指定

[example]
 $0 -s dev
EOS
exit 1
}

SCRIPT_DIR="$(cd $(dirname $0); pwd)"
PROJECT_ROOT="$(cd ${SCRIPT_DIR}/..; pwd)"
FRONT_DIR="$(cd ${PROJECT_ROOT}/front; pwd)"
source "${SCRIPT_DIR}/lib/utils.sh"

STAGE=
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help  ) usage;;
    -s | --stage ) shift;STAGE="$1";;
    -* | --*     ) error "$1 : 不正なオプションです" ;;
    *            ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage
[ -z "${STAGE}" ] && error "-s | --stage オプションを指定してください"

PROFILE_PATH="${PROJECT_ROOT}/profile/${STAGE}.yml"
[ -r "$PROFILE_PATH" ] || error "デプロイ用プロファイルが見つかりません: $PROFILE_PATH"

set -e

# nuxt app ビルド
cd $FRONT_DIR
export API_GATEWAY_BASE_PATH="/${STAGE}"
invoke npm install
invoke npm run generate

# serverless デプロイ
cd $PROJECT_ROOT
invoke npm install
invoke sls deploy --stage ${STAGE}