#!/bin/bash -l

function usage {
cat >&2 <<EOS
dockerイメージpushコマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
 -s | --stage <STAGE>: (required)
   pushするステージ名を指定(stg, prd, など)
 --build-only:
   ビルドのみを行う
 --no-cache:
   キャッシュを使わないでビルド
 --proxy:
   プロキシ設定を有効化
EOS
exit 1
}

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)
source "${SCRIPT_DIR}/lib/utils.sh"

APP_NAME=$(get_app_name ${PROJECT_ROOT}/app_name)

STAGE=
BUILD_OPTIONS=
BUILD_ONLY=
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help  ) usage;;
    -s | --stage ) shift;STAGE="$1";;
    --build-only ) BUILD_ONLY=1;;
    --no-cache   ) BUILD_OPTIONS="$BUILD_OPTIONS --no-cache";;
    --proxy      ) BUILD_OPTIONS="$BUILD_OPTIONS --build-arg proxy=$proxy --build-arg no_proxy=$no_proxy";;
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
AWS_PROFILE="default"
AWS_ACCOUNT_ID=$(aws --profile $AWS_PROFILE sts get-caller-identity --query 'Account' --output text)

info "AWS_REGION: $AWS_REGION"
info "AWS_PROFILE: $AWS_PROFILE"
info "AWS_ACCOUNT_ID: $AWS_ACCOUNT_ID"

aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
cd "$PROJECT_ROOT"
for image_name in lambda; do
  LOCAL_IMAGE="${APP_NAME}/${image_name}:latest"
  invoke docker build $BUILD_OPTIONS \
    --rm \
    --build-arg api_gateway_base_path=/${STAGE} \
    -f docker/lambda/Dockerfile \
    -t $LOCAL_IMAGE \
    .

  if [ -z "$BUILD_ONLY" ]; then
    REMOTE_IMAGE="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${APP_NAME}/${image_name}/${STAGE}:latest"
    invoke docker tag "$LOCAL_IMAGE" "$REMOTE_IMAGE"
    invoke docker push "$REMOTE_IMAGE"
  fi
done