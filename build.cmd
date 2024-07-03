$ErrorActionPreference = "Stop"
docker image rm varnav/acapi
docker build -t varnav/acapi --progress=plain . || exit /b
docker run --rm -it --entrypoint /app/prestart.sh varnav/acapi || exit /b

