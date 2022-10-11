FROM public.ecr.aws/lambda/python:3.8

ARG proxy
ARG no_proxy

ENV http_proxy=$proxy
ENV https_proxy=$proxy
ENV NO_PROXY=$no_proxy

RUN printenv

# update package
RUN yum update -y

# install nodejs
RUN curl -fsSL https://rpm.nodesource.com/setup_lts.x | bash -
RUN yum install -y nodejs

# pip install
COPY requirements.txt .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# nuxt generate
COPY front ${LAMBDA_TASK_ROOT}/front
RUN cd ${LAMBDA_TASK_ROOT}/front && \
    npm update -g npm && \
    npm install

ARG api_gateway_base_path
ENV API_GATEWAY_BASE_PATH=$api_gateway_base_path
RUN cd ${LAMBDA_TASK_ROOT}/front && \
    npm run generate

# copy api source
COPY api ${LAMBDA_TASK_ROOT}/api

CMD ["api.main.handler"]