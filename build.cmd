$ErrorActionPreference = "Stop"
docker build -t varnav/acapi --progress=plain . || exit /b
docker scout cves --only-severity critical,high varnav/acapi
docker run --rm -it --entrypoint /app/prestart.sh varnav/acapi || exit /b
docker push varnav/acapi