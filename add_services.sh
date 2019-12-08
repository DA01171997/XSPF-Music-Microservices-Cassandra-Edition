#python -mjson.tool

##########################################################################
########################Delete if Service/Route already exist#############
curl -i -X DELETE \
--url http://localhost:8001/routes/playlist-route

curl -i -X DELETE \
--url http://localhost:8001/services/api-v1-playlist-service

curl -i -X DELETE \
--url http://localhost:8001/routes/user-route

curl -i -X DELETE \
--url http://localhost:8001/services/api-v1-user-service

curl -i -X DELETE \
--url http://localhost:8001/routes/track-route

curl -i -X DELETE \
--url http://localhost:8001/services/api-v1-track-service

curl -i -X DELETE \
--url http://localhost:8001/routes/description-route

curl -i -X DELETE \
--url http://localhost:8001/services/api-v1-description-service

curl -i -X DELETE \
--url http://localhost:8001/routes/media-route

curl -i -X DELETE \
--url http://localhost:8001/services/api-v1-media


##########################################################################
echo
echo
echo "***** Add MinIo tracks service *****"
echo
echo

curl -i -v -X POST \
--url http://localhost:8001/services/ \
--data 'name=api-v1-media' \
--data 'url=http://127.0.0.1:9000/tracks/'

echo
echo
echo "-----add MinIo route"
echo
echo
curl -i -v -X POST \
  --url http://localhost:8001/services/api-v1-media/routes \
  --data 'hosts[]=127.0.0.1&hosts[]=localhost' \
  --data 'paths[]=/media/' \
  --data 'name=media-route' 


##########################################################################
echo
echo
echo "***** create playlist upstreams *****"
echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams \
    --data "name=playlist-v1-upstream"

echo
echo
echo "-----add playlist targets to upstream"
curl -i -v -X POST http://127.0.0.1:8001/upstreams/playlist-v1-upstream/targets \
  --data "target=127.0.0.1:5200"
  --data "weight=100"

echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams/playlist-v1-upstream/targets \
  --data "target=127.0.0.1:5201"
  --data "weight=100"

echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams/playlist-v1-upstream/targets \
  --data "target=127.0.0.1:5202"
  --data "weight=100"


echo
echo
echo "-----add playlist services"

curl -i -v -X POST \
--url http://localhost:8001/services/ \
--data 'name=api-v1-playlist-service' \
--data 'host=playlist-v1-upstream' \
--data 'path=/api/v1/collections/playlists'

echo
echo
echo "-----add  playlist route"
curl -i -v -X POST \
  --data 'name=playlist-route' \
  --url http://localhost:8001/services/api-v1-playlist-service/routes \
  --data 'hosts[]=127.0.0.1&hosts[]=localhost' \
  --data 'paths[]=/api/v1/collections/playlists' \
  

##########################################################################
echo
echo
echo "***** create user upstreams *****"
echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams \
    --data "name=user-v1-upstream"

echo
echo
echo "-----add user targets to upstream"
curl -i -v -X POST http://127.0.0.1:8001/upstreams/user-v1-upstream/targets \
  --data "target=127.0.0.1:5000"
  --data "weight=100"

echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams/user-v1-upstream/targets \
  --data "target=127.0.0.1:5001"
  --data "weight=100"

echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams/user-v1-upstream/targets \
  --data "target=127.0.0.1:5002"
  --data "weight=100"


echo
echo
echo "-----add user services"

curl -i -v -X POST \
--url http://localhost:8001/services/ \
--data 'name=api-v1-user-service' \
--data 'host=user-v1-upstream' \
--data 'path=/api/v1/users/'

echo
echo
echo "-----add  user route"
curl -i -v -X POST \
  --data 'name=user-route' \
  --url http://localhost:8001/services/api-v1-user-service/routes \
  --data 'hosts[]=127.0.0.1&hosts[]=localhost' \
  --data 'paths[]=/api/v1/users/' \

##########################################################################
echo
echo
echo "***** create track upstreams *****"
echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams \
    --data "name=track-v1-upstream"

echo
echo
echo "-----add track targets to upstream"
curl -i -v -X POST http://127.0.0.1:8001/upstreams/track-v1-upstream/targets \
  --data "target=127.0.0.1:5100"
  --data "weight=100"

echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams/track-v1-upstream/targets \
  --data "target=127.0.0.1:5101"
  --data "weight=100"

echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams/track-v1-upstream/targets \
  --data "target=127.0.0.1:5102"
  --data "weight=100"


echo
echo
echo "-----add track services"

curl -i -v -X POST \
--url http://localhost:8001/services/ \
--data 'name=api-v1-track-service' \
--data 'host=track-v1-upstream' \
--data 'path=/api/v1/collections/tracks'

echo
echo
echo "-----add  track route"
curl -i -v -X POST \
  --data 'name=track-route' \
  --url http://localhost:8001/services/api-v1-track-service/routes \
  --data 'hosts[]=127.0.0.1&hosts[]=localhost' \
  --data 'paths[]=/api/v1/collections/tracks' \

##########################################################################
echo
echo
echo "***** create description upstreams *****"
echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams \
    --data "name=description-v1-upstream"

echo
echo
echo "-----add description targets to upstream"
curl -i -v -X POST http://127.0.0.1:8001/upstreams/description-v1-upstream/targets \
  --data "target=127.0.0.1:5300"
  --data "weight=100"

echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams/description-v1-upstream/targets \
  --data "target=127.0.0.1:5301"
  --data "weight=100"

echo
echo
curl -i -v -X POST http://127.0.0.1:8001/upstreams/description-v1-upstream/targets \
  --data "target=127.0.0.1:5302"
  --data "weight=100"


echo
echo
echo "-----add description services"

curl -i -v -X POST \
--url http://localhost:8001/services/ \
--data 'name=api-v1-description-service' \
--data 'host=description-v1-upstream' \
--data 'path=/api/v1/descriptions/'

echo
echo
echo "-----add  description route"
curl -i -v -X POST \
  --data 'name=description-route' \
  --url http://localhost:8001/services/api-v1-description-service/routes \
  --data 'hosts[]=127.0.0.1&hosts[]=localhost' \
  --data 'paths[]=/api/v1/descriptions/' \