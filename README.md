* [A+ rated] SSL configuration with TLS 1.3 and HTTP/2

## Aircraft Database API

Returns data from [BaseStation.sqb](https://github.com/varnav/BaseStation.sqb).

Query example: ``

Response:

```json

```

## Run app quickly

```sh
poetry install
cd app
python -m uvicorn main:app --reload
```

Open `http://localhost:8000/docs`



## Run app in production

[Dockerfile](Dockerfile) will build necessary tools and run app behind nginx. You may use letsencrypt (default) or your own certs. You need to edit [nginx.conf](nginx.conf) for your own needs. Replace `changeme.com` with your domain name. Then you can build docker image and run it this way:

```sh
docker build -t mycoolcompany/acapi .
docker run -d --name acapi --restart on-failure:10 --security-opt no-new-privileges -p 80:80 -p 443:443 -v /etc/letsencrypt:/etc/letsencrypt mycoolcompany/acapi
```

## How to get letsencrypt cert

Run this on host VM:
```bash
docker stop acapi
certbot certonly --standalone -d yourdomain.com
``` 

