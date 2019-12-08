#!/bin/bash
rm music.db
rm track1.db
rm track2.db
rm track3.db
sudo apt install python3-pip
pip3 install --user -r requirements.txt
sqlite3 music.db < queries/initQueries/init_db.sql
sqlite3 track1.db < queries/initQueries/init_track1_db.sql
sqlite3 track2.db < queries/initQueries/init_track2_db.sql
sqlite3 track3.db < queries/initQueries/init_track3_db.sql
foreman start -m "users=3,tracks=3,playlists=3,descriptions=3,xspfApi=1"
