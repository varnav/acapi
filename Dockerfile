# Docs https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.description="acapi Web API"
LABEL org.opencontainers.image.licenses="SPDX-License-Identifier: MIT"
LABEL org.opencontainers.image.authors="Evgeny Varnavskiy <varnavruz@gmail.com>"
LABEL org.opencontainers.vcs-url="https://github.com/varnav/acapi"
LABEL org.opencontainers.docker.cmd="docker run -d --name acapi --restart on-failure:10 --security-opt no-new-privileges -p 80:80 -p 443:443 -v /etc/letsencrypt:/etc/letsencrypt mycoolcompany/acapi"
LABEL org.opencontainers.docker.cmd.test="docker run --rm -it --entrypoint /app/pytest.sh varnav/acapi"

ENV PORT=8000
ENV DEBIAN_FRONTEND=noninteractive
#ENV ACCESS_LOG=/var/log/gunicorn/access.log
#ENV ERROR_LOG=/var/log/gunicorn/error.log

WORKDIR /app

COPY ./app/pyproject.toml .

RUN set -ex && \
    mkdir /html && \
    python -m pip install --no-cache-dir -U pip && \
    python -m pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install && \
    apt-get update && \
    apt-get install --no-install-recommends -y wget nginx software-properties-common ca-certificates && \
    mkdir /tmp/acapi_temp && \
    mkdir /var/log/gunicorn && \
    chmod 777 /tmp/acapi_temp && \
    ln -s /tmp/acapi_temp /html/getfile && \
    python -m pip install --no-cache-dir pytest certbot certbot-nginx && \
    wget -q https://github.com/varnav/BaseStation.sqb/releases/download/latest/BaseStation.sqb.tar.xz && \
    tar xf BaseStation.sqb.tar.xz && \
    rm -f BaseStation.sqb.tar.xz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./html /html/
COPY nginx-no-tls.conf /etc/nginx/nginx.conf
COPY ./app/main.py ./app/prestart.sh ./app/test_main.py /app/

EXPOSE 80
