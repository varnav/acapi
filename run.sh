mkdir /etc/letsencrypt
docker stop acapi && docker rm acapi && docker pull varnav/acapi
docker run -d --name acapi -p 80:80 varnav/acapi
docker logs -f acapi
