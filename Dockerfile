FROM python:3.12

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

COPY ./app/requirements.txt .

RUN set -ex && \
    mkdir /html && \
    python -m pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    apt-get update && \
    apt-get install --no-install-recommends -y sqlite3 wget software-properties-common ca-certificates && \
    python -m pip install --no-cache-dir pytest && \
    wget -q https://github.com/varnav/BaseStation.sqb/releases/download/latest/BaseStation.sqb.tar.xz && \
    tar xf BaseStation.sqb.tar.xz && \
    rm -f BaseStation.sqb.tar.xz && \
    sqlite3 BaseStation.sqb "CREATE INDEX IF NOT EXISTS ix_aircraft_registration ON Aircraft(Registration);" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./html /html/
COPY ./app/app.py ./app/prestart.sh ./app/test_main.py /app/

EXPOSE 8000

WORKDIR /app

CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]