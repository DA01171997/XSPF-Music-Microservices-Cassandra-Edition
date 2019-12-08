#!/bin/bash

echo "This is test get all tracks"
curl --verbose\
	--request GET\
	--header 'Content-Type: application/json'\
	http://127.0.0.1:8000/api/v1/collections/tracks/all;
##done

echo "\n"
echo "\n"
echo "\n"

echo "This is get a track with an id. This is supposed to fail."
curl --verbose\
    --request GET\
    http://127.0.0.1:8000/api/v1/collections/tracks/1;
##done

echo
echo
echo

echo "This is get a track with an id. This is supposed to succeed."
curl --verbose\
    --request GET\
    http://127.0.0.1:8000/api/v1/collections/tracks/3c99e1e7-3b1a-4d4b-b2e9-ce49f896d051;#put a uuid here after retreiving all;
##done

echo
echo
echo

echo "This is delete a track with a certain id. This is supposed to fail."
curl --verbose\
    --request DELETE\
    http://127.0.0.1:8000/api/v1/collections/tracks/1;
#done

echo 
echo
echo

echo "This is delete a track with a certain id. This is supposed to succeed."
curl --verbose\
    --request DELETE\
    http://127.0.0.1:8000/api/v1/collections/tracks/3c99e1e7-3b1a-4d4b-b2e9-ce49f896d051;#put a uuid here after retreiving all;
#done

echo
echo
echo

echo "This is delete a track with a certain id after its already been deleted. This is supposed to fail."
curl --verbose\
    --request DELETE\
    http://127.0.0.1:8000/api/v1/collections/tracks/3c99e1e7-3b1a-4d4b-b2e9-ce49f896d051;#put a uuid here after retreiving all;
#done

echo 
echo
echo

echo "This is supposed to get a track with the provided arguments. This is supposed to fail."
curl --verbose\
    --request GET\
    http://127.0.0.1:8000/api/v1/collections/tracks?trackID=1;
#done

echo
echo
echo

echo "This is supposed to get a track with the provided arguments. This is supposed to succeed being provided a trackTitle."
curl --verbose\
    --request GET\
    http://127.0.0.1:8000/api/v1/collections/tracks?trackTitle=Track%20title%2000;
#done

echo
echo
echo

echo "This is supposed to get a track with the provided arguments. This is supposed to succeed being provided with a trackAlbum."
curl --verbose\
    --request GET\
    http://127.0.0.1:8000/api/v1/collections/tracks?trackAlbum=The%2000%20album;
#done

echo
echo
echo

echo "This is supposed to get a track with the provided arguments. This is supposed to succeed being provided with a trackArtist."
curl --verbose\
    --request GET\
    http://127.0.0.1:8000/api/v1/collections/tracks?trackArtist=The%2000%20artist;
#done

echo
echo
echo

echo "This is supposed to post the track with the given json. This is supposed to fail b/c malformed."
curl --verbose\
    --request POST\
    --header 'Content-Type: application/json'\
	--data @trackTest2.json \
    http://127.0.0.1:8000/api/v1/collections/tracks;
#done

echo
echo
echo

echo "This is supposed to post the track with the given json. This is supposed to succeed even with no trackArt provided."
curl --verbose\
    --request POST\
    --header 'Content-Type: application/json'\
	--data @trackTest.json \
    http://127.0.0.1:8000/api/v1/collections/tracks;
#done

echo
echo
echo

echo "This is supposed to post the track with the given json. This is supposed to succeed with trackArt provided."
curl --verbose\
    --request POST\
    --header 'Content-Type: application/json'\
	--data @trackTest3.json \
    http://127.0.0.1:8000/api/v1/collections/tracks;
#done

echo
echo
echo

echo "This is supposed to patch the track with the given json. This is supposed to succeed."
curl --verbose\
    --request PATCH\
    --header 'Content-Type: application/json'\
	--data @trackTest4.json \
    http://127.0.0.1:8000/api/v1/collections/tracks;
#done

echo
echo
echo

echo "This is supposed to patch the track with the given json. This is supposed to fail because malformed."
curl --verbose\
    --request PATCH\
    --header 'Content-Type: application/json'\
	--data @trackTest3.json \
    http://127.0.0.1:8000/api/v1/collections/tracks;
#done