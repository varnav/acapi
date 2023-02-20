$ErrorActionPreference = "Stop"
docker build -t varnav/acapi --progress=plain . || exit /b
docker run --rm -it --entrypoint /app/pytest.sh varnav/acapi || exit /b
docker push varnav/acapi