#!/bin/bash -ex
#docker pull varnav/acapi
docker run --rm -it --entrypoint /app/prestart.sh varnav/acapi