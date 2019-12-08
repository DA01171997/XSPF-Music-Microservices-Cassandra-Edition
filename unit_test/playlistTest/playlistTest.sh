#!/bin/bash

echo "This is test get all tracks"
curl --verbose\
	--request GET\
	--header 'Content-Type: application/json'\
	http://127.0.0.1:8000/api/v1/collections/playlists/all
#done

echo
echo
echo

echo "This is get a playlist with an id. This is supposed to fail."
curl --verbose\
    --request GET\
    http://127.0.0.1:8000/api/v1/collections/playlists/9999
#done

echo
echo
echo

echo "This is get a playlist with an id. This is supposed to succeed."
curl --verbose\
    --request GET\
    http://127.0.0.1:8000/api/v1/collections/tracks/1
#done

echo
echo
echo

echo "This is to delete a playlist with a certain id. This is supposed to fail."
curl --verbose \
    --request DELETE \
    --header 'Content-Type: application/json' \
    http://127.0.0.1:8000/api/v1/collections/playlists/9999
#done

echo
echo
echo

echo "This is to delete a playlist with a certain id. This is supposed to succeed."
curl --verbose \
    --request DELETE \
    --header 'Content-Type: application/json' \
    http://127.0.0.1:8000/api/v1/collections/playlists/1
#done

echo
echo
echo

echo "This is to delete a playlist with a certain id. This is supposed to fail."
curl --verbose \
    --request DELETE \
    --header 'Content-Type: application/json' \
    http://127.0.0.1:8000/api/v1/collections/playlists/1
#done

echo
echo
echo

echo "This is to get a playlist with the provided arguments. This is supposed to fail."
curl --verbose \
    --request GET \
    --header 'Content-Type: application/json' \
    http://127.0.0.1:8000/api/v1/collections/playlists
#done

echo
echo
echo

echo "This is to get a playlist with the provided arguments. This is supposed to succeed."
curl --verbose \
    --request GET \
    --header 'Content-Type: application/json' \
    http://127.0.0.1:8000/api/v1/collections/playlists?playID=2
#done

echo
echo
echo

echo "This is to get a playlist with the provided arguments. This is supposed to succeed."
curl --verbose \
    --request GET \
    --header 'Content-Type: application/json' \
    http://127.0.0.1:8000/api/v1/collections/playlists?playTitle=Playlist%2002
#done

echo
echo
echo

echo "This is to get a playlist with the provided arguments. This is supposed to succeed."
curl --verbose \
    --request GET \
    --header 'Content-Type: application/json' \
    http://127.0.0.1:8000/api/v1/collections/playlists?userName=WassupMan404
#done

echo
echo
echo

echo "This is to post a playlist with the provided json. This is supposed to succeed."
curl --verbose \
    --request POST \
    --header 'Content-Type: application/json' \
    --data @playlistTest1.json \
    http://127.0.0.1:8000/api/v1/collections/playlists
#done

echo
echo
echo

echo "This is to post a playlist with the provided json. This is supposed to succeed w/o a playDesc."
curl --verbose \
    --request POST \
    --header 'Content-Type: application/json' \
    --data @playlistTest3.json \
    http://127.0.0.1:8000/api/v1/collections/playlists
#done

echo
echo
echo

echo "This is to post a playlist with the provided json. This is supposed to fail b/ malformed."
curl --verbose \
    --request POST \
    --header 'Content-Type: application/json' \
    --data @playlistTest2.json \
    http://127.0.0.1:8000/api/v1/collections/playlists
#done