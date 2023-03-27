# If used outside of Docker

curl -s -o BaseStation.sqb.tar.gz https://github.com/varnav/BaseStation.sqb/releases/download/latest/BaseStation.sqb.tar.gz
tar xf BaseStation.sqb.tar.gz
rm -f BaseStation.sqb.tar.gz
poetry install
python -m pytest .