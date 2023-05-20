#!/bin/bash

rm -f ReleasableAircraft.zip
echo "Downloading..."
wget -q https://registry.faa.gov/database/ReleasableAircraft.zip
unzip ReleasableAircraft.zip MASTER.txt
echo "Importing..."
echo -e ".separator ","\n.import MASTER.txt faadb" | sqlite3 faadb.db
echo "Cleanup..."
rm -f ReleasableAircraft.zip MASTER.txt