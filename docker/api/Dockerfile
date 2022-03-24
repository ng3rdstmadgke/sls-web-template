FROM python:3.8.12-slim-bullseye

ARG proxy
ARG no_proxy

ENV http_proxy=$proxy
ENV https_proxy=$proxy
ENV NO_PROXY=$no_proxy

RUN printenv

RUN apt update && \
    apt install -y locales gcc libmariadb-dev unzip jq curl&& \
    apt install -y iputils-ping net-tools default-mysql-client less groff && \
    apt clean

RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8

RUN cd /tmp && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.0.30.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -r aws awscliv2.zip

RUN curl -sL https://deb.nodesource.com/setup_lts.x | bash -
RUN apt update && \
    apt install -y nodejs && \
    apt clean

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY front /opt/app/front
RUN cd /opt/app/front && \
    npm update -g npm && \
    npm install && \
    npx nuxt generate && \
    npm cache clean  --force

COPY api /opt/app/api
RUN  rm -rf /opt/app/api/front && \
     mv /opt/app/front/dist /opt/app/api/front && \
     rm -rf /opt/app/front ~/npm

COPY bin /opt/app/bin
COPY docker/api/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN ls /opt/app/api/front
CMD ["/usr/local/bin/entrypoint.sh"]
