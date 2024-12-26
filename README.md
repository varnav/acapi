## Aircraft Database API

Returns aircraft data from [BaseStation.sqb](https://github.com/varnav/BaseStation.sqb)

Query example: `http://127.0.0.1:8000/api/v1/ac/reg/JA739J`

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

[Dockerfile](Dockerfile) will build necessary tools and run app this way:

```sh
docker build -t mycoolcompany/acapi .
docker run -d --name acapi --restart on-failure:10 --security-opt no-new-privileges -p 8000:8000 mycoolcompany/acapi
```

## Run tests and then app in debugging mode

```sh
docker run -it --rm --entrypoint /app/prestart.sh mycoolcompany/acapi
docker run -it --rm -p 8000:8000 mycoolcompany/acapi
```

## Run app in Kubernetes

`kubectl apply -f .\acapi-k8s.yml`

This will deploy 2 instances of backend and 1 instance of varnish cache on port 30080
