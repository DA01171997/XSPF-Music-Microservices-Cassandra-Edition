#!/bin/bash
sudo apt install python3-pip
pip3 install --user -r requirements.txt
docker exec -i scylla cqlsh < "cql/init.cql"
foreman start -m "users=3,tracks=3,playlists=3,descriptions=3,xspfApi=1"