#!/bin/bash
function usage {
cat >&2 <<EOS
nuxtjsのビルドスクリプト

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -s | --stage <STAGE_NAME>:
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

STAGE_NAME=
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help  ) usage;;
    -s | --stage ) shift;STAGE_NAME="$1";;
    -* | --*     ) error "$1 : 不正なオプションです" ;;
    *            ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage

set -e
cd $FRONT_DIR
[ -n "$STAGE_NAME" ] && export API_GATEWAY_ROOT_PATH="/${STAGE_NAME}/"
invoke npm install
invoke npm run generate
invoke rm -rf ${PROJECT_ROOT}/api/front
invoke cp -r ${PROJECT_ROOT}/front/dist ${PROJECT_ROOT}/api/front
