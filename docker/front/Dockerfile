FROM node:16-bullseye-slim

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

RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY front .
RUN npm update -g npm && npm install && npm prune

COPY docker/front/front-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/front-entrypoint.sh
CMD ["/usr/local/bin/front-entrypoint.sh"]