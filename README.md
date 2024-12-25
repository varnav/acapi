## Aircraft Database API

Returns aircraft data from [BaseStation.sqb](https://github.com/varnav/BaseStation.sqb)

Query example: `http://127.0.0.1:8000/api/v1/ac/getbyreg?reg=JA739J`

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

## Run app in debugging mode

```sh
docker run -it --rm -p 8000:8000 mycoolcompany/acapi
```

## Run app in Kubernetes

1. Install [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/deploy/)
2. kubectl apply -f .\acapi-k8s.yml
