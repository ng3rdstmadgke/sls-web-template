FROM nginx:1.21.5

ARG proxy
ARG no_proxy

ENV http_proxy=$proxy
ENV https_proxy=$proxy
ENV NO_PROXY=$no_proxy

RUN printenv

RUN apt update && \
    apt install -y locales
#   apt install -y iputils-ping net-tools

RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

COPY ./docker/nginx/config/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/config/default.conf /etc/nginx/conf.d/default.conf