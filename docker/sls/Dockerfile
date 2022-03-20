# Docker内でdockerコマンドを利用するためのイメージ: https://hub.docker.com/_/docker
# Docker outside of Docker: https://esakat.github.io/esakat-blog/posts/docker-in-docker/
FROM docker:20.10.12-dind

ARG proxy
ARG no_proxy

ENV http_proxy=$proxy
ENV https_proxy=$proxy
ENV NO_PROXY=$no_proxy
# ~/.aws/configを利用する場合は有効化
#ENV AWS_SDK_LOAD_CONFIG 1

RUN printenv

COPY sls_version .
RUN apk update && apk add --no-cache nodejs npm
RUN npm install -g serverless@`cat sls_version`

RUN mkdir /opt/sls
WORKDIR /opt/sls
COPY package.json .
COPY package-lock.json .
RUN npm install
COPY . .