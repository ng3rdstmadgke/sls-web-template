#!/bin/bash
function usage {
cat >&2 <<EOS
shell起動コマンド

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
HOST_UID=${LOCAL_UID}
HOST_GID=${LOCAL_GID}

UNAME="app"

# グループIDを指定してグループを作成
# -g: グループIDを指定する
groupadd -g $HOST_GID $UNAME

# ユーザーIDを指定してグループを作成
# -u: ユーザーIDを指定
# -o: ユーザーIDが同じユーザーの作成を許す
# -m: ホームディレクトリを作成する
# -g: ユーザーが属するプライマリグループを指定する(グループID or グループ名)
# -s: ログインシェルを指定する
useradd -u $HOST_UID -o -m -g $HOST_GID -s /bin/bash $UNAME
export HOME=/home/$UNAME

# マウント先のを所有者作成したユーザーとグループに変更
chown -R $HOST_UID:$HOST_GID /opt/app

# 作成したユーザーでアプリケーションサーバーを起動
exec su $UNAME