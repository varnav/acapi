## Aircraft Database API

Returns aircraft data from [BaseStation.sqb](https://github.com/varnav/BaseStation.sqb)

Query example: `http://127.0.0.1/api/v1/ac/getbyreg?reg=JA739J`

Response:

```json
[
  {
    "ModeS": "868078",
    "Registration": "JA739J",
    "ICAOTypeCode": "B77W",
    "OperatorFlagCode": "JAL",
    "Manufacturer": "BOEING",
    "Type": "777 346ER",
    "RegisteredOwners": "Japan Airlines"
  }
]
```

## Run app quickly

```sh
cd app
poetry install
python -m uvicorn main:app --reload
```

Open `http://localhost:8000/docs`



## Run app in production

[Dockerfile](Dockerfile) will build necessary tools and run app behind nginx. You may use letsencrypt, your own certs, or use without TLS (default). You need to edit [nginx.conf](nginx.conf) for your own needs. Replace `changeme.com` with your domain name. Then you can build docker image and run it this way:

```sh
docker build -t mycoolcompany/acapi .
docker run -d --name acapi --restart on-failure:10 --security-opt no-new-privileges -p 80:80 -p 443:443 -v /etc/letsencrypt:/etc/letsencrypt mycoolcompany/acapi
```

## How to get letsencrypt cert

Run this on host machine:
```bash
docker stop acapi
certbot certonly --standalone -d yourdomain.com
``` 

