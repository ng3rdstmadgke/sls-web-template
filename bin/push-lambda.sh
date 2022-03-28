#!/bin/bash -l

function usage {
cat >&2 <<EOS
dockerイメージpushコマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -t | --tag <TAG>:
   イメージのタグを指定(default=latest)
 -s | --stage <STAGE>: (required)
   pushするステージ名を指定(stg, prd, など)
EOS
exit 1
}

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
source "${SCRIPT_DIR}/lib/utils.sh"

APP_NAME=$(get_app_name ${PROJECT_ROOT}/app_name)

TAG=latest
STAGE=
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help  ) usage;;
    -t | --tag   ) shift;TAG="$1";;
    -s | --stage ) shift;STAGE="$1";;
    -* | --*     ) error "$1 : 不正なオプションです" ;;
    *            ) args+=("$1");;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage
[ -z "${STAGE}" ] && error "-s | --stage オプションが指定されていません"

set -e
trap 'echo "[$BASH_SOURCE:$LINENO] - "$BASH_COMMAND" returns not zero status"' ERR

AWS_REGION="ap-northeast-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

info "AWS_REGION: $AWS_REGION"
info "AWS_ACCOUNT_ID: $AWS_ACCOUNT_ID"

aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

for image_name in lambda; do
  LOCAL_IMAGE="${APP_NAME}/${image_name}:latest"
  REMOTE_IMAGE="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${APP_NAME}/${image_name}/${STAGE}:${TAG}"
  invoke docker tag "$LOCAL_IMAGE" "$REMOTE_IMAGE"
  invoke docker push "$REMOTE_IMAGE"
done