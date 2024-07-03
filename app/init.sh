# If used outside of Docker
set -ex
if [ ! -f "BaseStation.sqb" ]; then
    curl -s -L -o BaseStation.sqb.tar.gz https://github.com/varnav/BaseStation.sqb/releases/download/latest/BaseStation.sqb.tar.gz
    tar xf BaseStation.sqb.tar.gz
    rm -f BaseStation.sqb.tar.gz
    # curl -s -L -o ReleasableAircraft.zip https://registry.faa.gov/database/ReleasableAircraft.zip
    # unzip ReleasableAircraft.zip MASTER.txt
    # echo -e ".separator ","\n.import MASTER.txt faadb" | sqlite3 BaseStation.sqb
    # rm -f ReleasableAircraft.zip MASTER.txt
else
    echo "BaseStation.sqb already exists"
fi

poetry install
python -m pytest .
exit