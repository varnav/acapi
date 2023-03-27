# If used outside of Docker

curl -s -o BaseStation.sqb.tar.xz https://github.com/varnav/BaseStation.sqb/releases/download/latest/BaseStation.sqb.tar.xz
tar xf BaseStation.sqb.tar.xz
rm -f BaseStation.sqb.tar.xz
python -m pytest /app