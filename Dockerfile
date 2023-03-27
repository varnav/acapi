# Docs https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

LABEL Maintainer = "Evgeny Varnavskiy <varnavruz@gmail.com>"
LABEL Description="acapi Web API"
LABEL License="MIT License"

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.vcs-url="https://github.com/varnav/acapi"
LABEL org.label-schema.docker.cmd="docker run -d --name acapi --restart on-failure:10 --security-opt no-new-privileges -p 80:80 -p 443:443 -v /etc/letsencrypt:/etc/letsencrypt mycoolcompany/acapi"
LABEL org.label-schema.docker.cmd.test="docker run --rm -it --entrypoint /app/pytest.sh varnav/acapi"

ENV PORT=8000
ENV DEBIAN_FRONTEND=noninteractive
#ENV ACCESS_LOG=/var/log/gunicorn/access.log
#ENV ERROR_LOG=/var/log/gunicorn/error.log

COPY ./pyproject.toml .

RUN set -ex && \
    mkdir /html && \
    python -m pip install -U pip && \
    python -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

RUN apt-get update && apt-get install --no-install-recommends -y wget nginx software-properties-common ca-certificates && \
    mkdir /tmp/acapi_temp && \
    mkdir /var/log/gunicorn && \
    chmod 777 /tmp/acapi_temp && \
    ln -s /tmp/acapi_temp /html/getfile && \
    python -m pip install tailon pytest certbot certbot-nginx && \
    cd /app && \
    wget -q https://github.com/varnav/BaseStation.sqb/releases/download/latest/BaseStation.sqb.tar.xz && \
    tar xf BaseStation.sqb.tar.xz && \
    rm -f BaseStation.sqb.tar.xz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./html /html/
COPY nginx-no-tls.conf /etc/nginx/nginx.conf
COPY ./app/main.py ./app/prestart.sh ./app/pytest.sh ./app/test_main.py /app/

EXPOSE 80
