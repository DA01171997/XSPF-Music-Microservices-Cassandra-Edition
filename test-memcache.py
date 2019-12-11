from pymemcache.client import base
from pymemcache import fallback
import json


def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2

def json_deserializer(key, value, flags):
   if flags == 1:
       return value
   if flags == 2:
       return json.loads(value)
   raise Exception("Unknown serialization format")

client = base.Client(('localhost', 11211),serializer=json_serializer,deserializer=json_deserializer)

playTitle = "Playlist 0123"
key = playTitle.replace(" ", "_")
# print(key)
cache = client.get(key)
if cache is None:
    client.set(key,[{"message":"test"},{"dfdsf":"dfdsfdd"}],expire=10)
    print("Not cached")
else:
    print(cache)
    print("cached")

# @app.route("/api/v1/collections/playlists/<string:playTitle>.xspf", methods = ['GET'])
# def generate_xspf(playTitle):
#     try:
#         key = playTitle
#         key = key.replace(" ", "_")
#         client = base.Client(('localhost', 11211),serializer=json_serializer,deserializer=json_deserializer)
#         playlistURL = "http://localhost:8000/api/v1/collections/playlists/" + playTitle
#         cache = client.get(key)
#         if cache is None:
#             cacheList=[]
#             results = requests.get(playlistURL).json()
#             playlist = results[0]
#             tracks = requests.get("http://localhost:8000/api/v1/collections/tracks/all").json()
#             if playlist == {'message': 'This resource does not exist.'}:
#                 raise exceptions.NotFound
#             if tracks == {'message': 'This resource does not exist.'}:
#                 raise exceptions.NotFound
#             tracklist = getPlayListURLs(playlist)
#             cacheList.append(tracklist)
#             cacheList.append(tracks)
#             cacheList.append(playlist)
#             client.set(key, cacheList, expire=60)
#             xspf_playlist = getTrackInfoFromURL(tracklist, tracks, playlist)
#         else:
#             tracklist = cache[0]
#             tracks = cache[1]
#             playlist = cache[2]
#             xspf_playlist = getTrackInfoFromURL(tracklist, tracks, playlist)
#         return xspf_playlist.toXml(), status.HTTP_200_OK
#     except Exception as e:
#         return { 'error': str(e) }, status.HTTP_404_NOT_FOUND