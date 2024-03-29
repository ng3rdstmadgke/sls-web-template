FROM python:3.8.12-slim-bullseye

ARG proxy
ARG no_proxy

ENV http_proxy=$proxy
ENV https_proxy=$proxy
ENV NO_PROXY=$no_proxy

RUN printenv

RUN apt update && \
    apt install -y locales gcc libmariadb-dev unzip jq curl && \
    apt install -y iputils-ping net-tools default-mysql-client less groff && \
    apt clean

RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN cd /tmp && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.0.30.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -r aws awscliv2.zip

RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY api /opt/app/api
COPY bin /opt/app/bin

COPY docker/api/*-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/*-entrypoint.sh

ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID app && \
    useradd --home-dir /opt/app --no-create-home -s /bin/bash -u $UID -g $GID app
CMD ["/usr/local/bin/api-entrypoint.sh"]
