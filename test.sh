#!/bin/bash -ex
#docker pull varnav/acapi
docker run --rm -it --entrypoint /app/pytest.sh varnav/acapi