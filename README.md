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

```bash
# 開発用イメージビルド
./bin/build.sh


# http://localhost:3000/
./bin/run.sh
```
