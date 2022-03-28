# インストール

```bash
# nvm install
# https://github.com/nvm-sh/nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

# node.jsの最新のltsをインストール
nvm install --lts
nvm use --lts
node -v
npm -v

# npm update
npm update -g npm

# serverless install
cd sls-web-template
npm install
```

# デプロイ

```bash
STAGE_NAME=mi1

# プロファイル作成
cp ./profile/sample.yml ./profile/${STAGE_NAME}.yml
vim ./profile/${STAGE_NAME}.yml

# デプロイ
./bin/deploy.sh --stage mi1
```

# 開発環境
## 開発サーバー起動

```bash
# 開発用イメージビルド
./bin/build.sh

# 開発用データベース起動
./bin/run-mysql.sh -d

# テスト
./bin/test.sh

# アプリ起動
./bin/run.sh -e local.env

# アクセス
# http://localhost:3000/
# http://localhost:8000/api/docs
```

## テスト

```bash
# 開発用イメージビルド
./bin/build.sh

# 開発用データベース起動
./bin/run-mysql.sh -d

# テスト
./bin/test.sh
```

# 運用

## オペレーションshell起動

```bash
# 開発用データベース起動
./bin/run-mysql.sh -d

# オペレーション用shell起動
./bin/shell.sh -e <ENV_PATH>

```

## マイグレーション(オペレーションshell内での操作)

```bash
# DB作成
./bin/lib/create-database.sh

# マイグレーション: 履歴確認
./bin/lib/alembic.sh history -v

# マイグレーション: 最新バージョンにアップグレード
./bin/lib/alembic.sh upgrade head

# マイグレーション: 次のバージョンにアップグレード
./bin/lib/alembic.sh upgrade +1

# マイグレーション: 最初のバージョンにダウングレード
./bin/lib/alembic.sh downgrade base

# マイグレーション: 次のバージョンにダウングレード
./bin/lib/alembic.sh downgrade -1

# マイグレーション: マイグレーションファイル生成
./bin/lib/alembic.sh revision --autogenerate -m "message"
```

## DBログイン(オペレーションshell内での操作)

```bash
# DB作成
./bin/lib/create-database.sh

# mysql ログイン
./bin/lib/mysql.sh
```

## マネジメントコマンド(オペレーションshell内での操作)

```bash
# ヘルプ
./bin/lib/manage.sh

# スーパーユーザー作成
./bin/lib/manage.sh create_user admin --superuser

# 通常ユーザー作成
./bin/lib/manage.sh create_user user1
./bin/lib/manage.sh create_user user2

# ロール作成
./bin/lib/manage.sh create_role ItemAdminRole

# ロールのアタッチ
./bin/lib/manage.sh attach_role user1 ItemAdminRole

# ロールのデタッチ
./bin/lib/manage.sh detach_role user1 ItemAdminRole
```