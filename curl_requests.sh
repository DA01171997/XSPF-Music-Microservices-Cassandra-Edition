#!/bin/bash

for u in json/add_user*; do \
curl --verbose\
	--request POST\
	--header 'Content-Type: application/json'\
	--data @$u\
	http://127.0.0.1:8000/api/v1/users/register;
done

for t in json/add_track*; do \
curl --verbose\
	--request POST\
	--header 'Content-Type: application/json'\
	--data @$t\
	http://127.0.0.1:8000/api/v1/collections/tracks;
done

for p in json/add_playlist*; do \
curl --verbose\
	--request POST\
	--header 'Content-Type: application/json'\
	--data @$p\
	http://127.0.0.1:8000/api/v1/collections/playlists;
done

for d in json/add_description*; do \
curl --verbose\
	--request POST\
	--header 'Content-Type: application/json' \
	--data @$d \
	http://127.0.0.1:8000/api/v1/descriptions/;
done
