# If used outside of Docker
set -ex
if [ ! -f "BaseStation.sqb" ]; then
    curl -s -L -o BaseStation.sqb.tar.gz https://github.com/varnav/BaseStation.sqb/releases/download/latest/BaseStation.sqb.tar.gz
    tar xf BaseStation.sqb.tar.gz
    rm -f BaseStation.sqb.tar.gz
else
    echo "BaseStation.sqb already exists"
fi

poetry install
python -m pytest .