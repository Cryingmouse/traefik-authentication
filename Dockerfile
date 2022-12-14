FROM python:3.9.16-alpine3.17 as build-env

WORKDIR /root

COPY requirements.txt .
COPY dist/dsm_auth*.whl .

RUN set -x \
  && echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.15/main/" > /etc/apk/repositories \
  && apk add --no-cache --virtual .build-deps \
      bash \
      drill \
      bind-tools \
      g++ \
      libc-dev \
      python3-dev \
      libffi libffi-dev \
      openssl-dev \
      make \
      mariadb-dev \
  && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt \
  && pip3 install dsm_auth*.whl


FROM python:3.9.16-alpine3.17
WORKDIR /root

COPY --from=build-env /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

RUN set -x \
  && echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.15/main/" > /etc/apk/repositories \
  && apk add --no-cache --virtual .build-deps \
      bash \
      mysql-client \
      redis \
      curl \
      mariadb-dev \