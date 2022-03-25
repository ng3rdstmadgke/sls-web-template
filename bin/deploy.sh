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
[ -z "${STAGE_NAME}" ] && error "-s | --stage オプションを指定してください"

set -e

${SCRIPT_DIR}/nuxt-generate.sh --stage ${STAGE_NAME}
invoke sls deploy --stage ${STAGE_NAME}
