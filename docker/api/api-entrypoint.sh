#!/bin/bash
function usage {
cat >&2 <<EOS
nuxtアプリ起動コマンド

[usage]
 $0 [options]

[options]
 -h | --help:
   ヘルプを表示
EOS
exit 1
}

while [ "$#" != 0 ]; do
  case $1 in
    -h | --help      ) usage;;
    -* | --*         ) echo "$1 : 不正なオプションです" >&2; exit 1;;
    *                ) args+=("$1");;
  esac
  shift
done

# HOST_UID=${変数名:-デフォルト値}
HOST_UID=${LOCAL_UID:-1000}
HOST_GID=${LOCAL_GID:-1000}

# ホスト側の実行ユーザーと同一のUID, GIDを持つユーザーを作成
echo "Starting with UID : $HOST_UID, GID: $HOST_GID"
useradd -u $HOST_UID -o -m app
groupmod -g $HOST_GID app
export HOME=/home/app

chown -R app:app /opt/app
# 作成したユーザーでアプリケーションサーバーを起動
echo "printenv && uvicorn api.main:app --log-config api/log_config.yml --reload"
exec su app -c "printenv && uvicorn api.main:app --log-config api/log_config.yml --reload"