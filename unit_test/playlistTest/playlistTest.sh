#!/bin/bash

echo "1.This is test get all tracks"
curl --verbose\
	--request GET\
	--header 'Content-Type: application/json'\
	http://127.0.0.1:8000/api/v1/collections/playlists/all
#done

echo
echo
echo

echo "2.This is get a playlist with an id. This is supposed to fail."
curl --verbose\
    --request GET\
    http://127.0.0.1:8000/api/v1/collections/playlists/Playlist%2009
#done

echo
echo
echo

echo "3.This is get a playlist with an id. This is supposed to succeed."
curl --verbose\
    --request GET\
    http://127.0.0.1:8000/api/v1/collections/playlists/Playlist%2000
#done

echo
echo
echo

echo "4.This is to delete a playlist with a certain id. This is supposed to fail."
curl --verbose \
    --request DELETE \
    --header 'Content-Type: application/json' \
    http://127.0.0.1:8000/api/v1/collections/playlists/Playlist%2009
#done

echo
echo
echo

echo "5.This is to delete a playlist with a certain id. This is supposed to succeed."
curl --verbose \
    --request DELETE \
    --header 'Content-Type: application/json' \
    http://127.0.0.1:8000/api/v1/collections/playlists/Playlist%2000
#done

echo
echo
echo

echo "6.This is to delete a playlist with a certain id. This is supposed to fail."
curl --verbose \
    --request DELETE \
    --header 'Content-Type: application/json' \
    http://127.0.0.1:8000/api/v1/collections/playlists/Playlist%2000
#done

# echo
# echo
# echo

# echo "7.This is to get a playlist with the provided arguments. This is supposed to fail."
# curl --verbose \
#     --request GET \
#     --header 'Content-Type: application/json' \
#     http://127.0.0.1:8000/api/v1/collections/playlists
# #done

# echo
# echo
# echo

# echo "8.This is to get a playlist with the provided arguments. This is supposed to succeed."
# curl --verbose \
#     --request GET \
#     --header 'Content-Type: application/json' \
#     http://127.0.0.1:8000/api/v1/collections/playlists?playID=2
# #done

# echo
# echo
# echo

# echo "9.This is to get a playlist with the provided arguments. This is supposed to succeed."
# curl --verbose \
#     --request GET \
#     --header 'Content-Type: application/json' \
#     http://127.0.0.1:8000/api/v1/collections/playlists?playTitle=Playlist%2002
# #done

# echo
# echo
# echo

# echo "10.This is to get a playlist with the provided arguments. This is supposed to succeed."
# curl --verbose \
#     --request GET \
#     --header 'Content-Type: application/json' \
#     http://127.0.0.1:8000/api/v1/collections/playlists?userName=WassupMan404
# #done

echo
echo
echo

echo "7.This is to post a playlist with the provided json. This is supposed to succeed."
curl --verbose \
    --request POST \
    --header 'Content-Type: application/json' \
    --data @playlistTest1.json \
    http://127.0.0.1:8000/api/v1/collections/playlists
#done

echo
echo
echo

echo "8.This is to post a playlist with the provided json. This is supposed to succeed w/o a playDesc."
curl --verbose \
    --request POST \
    --header 'Content-Type: application/json' \
    --data @playlistTest3.json \
    http://127.0.0.1:8000/api/v1/collections/playlists
#done

echo
echo
echo

echo "9.This is to post a playlist with the provided json. This is supposed to fail b/ malformed."
curl --verbose \
    --request POST \
    --header 'Content-Type: application/json' \
    --data @playlistTest2.json \
    http://127.0.0.1:8000/api/v1/collections/playlists
#done