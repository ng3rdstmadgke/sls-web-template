FROM python:3.8.12-slim-bullseye


ARG proxy
ARG no_proxy

ENV http_proxy=$proxy
ENV https_proxy=$proxy
ENV NO_PROXY=$no_proxy
# ~/.aws/configを利用する場合は有効化
#ENV AWS_SDK_LOAD_CONFIG 1

RUN printenv

RUN apt update && apt install -y curl jq locales
RUN curl -sL https://deb.nodesource.com/setup_lts.x | bash -
RUN apt update && \
    apt install -y nodejs && \
    apt clean

RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

COPY sls_version .

RUN npm update -g npm && \
    npm install -g serverless@`cat sls_version`

RUN mkdir /opt/sls
WORKDIR /opt/sls