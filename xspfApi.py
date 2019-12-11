import json, requests
from xspf import xspf
from flask import request, jsonify, Response
import flask_api
from flask_api import status, exceptions
import xml.dom.minidom
from requests.exceptions import HTTPError

from pymemcache.client import base
from pymemcache import fallback

app = flask_api.FlaskAPI(__name__,static_url_path='')
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

def getPlayListByID(id, playlists):
    for playlist in playlists:
        if playlist['playID'] == id:
            return playlist

def getDescriptionByUrl(playUserUserName, url):
    url = "http://127.0.0.1:8000/api/v1/descriptions/users/{}/descriptions?trackMediaURL={}".format(playUserUserName,url)
    key = playUserUserName + url + "description"
    key = key.replace(" ", "_")
    cache = client.get(key)
    if cache is None:
        response = requests.get(url)
        if response.status_code == 200:
            desc = response.json()
            desc = desc[0]['descriptionDesc']
        else:
            desc = ""
        client.set(key, desc, expire=60)
        return desc
    else:
        return cache.decode("utf-8")

def getPlayListURLs(playlist):
    tracklist = playlist['playListOfTracks']
    return tracklist

def getTrackInfoFromURL(urls, tracks, playlist):
    x = xspf.Xspf()
    x.title = playlist['playTitle']
    x.creator = playlist['playUserUserName']
    x.annotation = playlist['playDesc']
    for url in urls:
        tr = xspf.Track()
        for track in tracks:
            if url in track['trackMediaURL']:
                tr.creator = track['trackArtist']
                tr.title = track['trackTitle']
                tr.album = track['trackAlbum']
                tr.duration = str(track['trackLength']) # cast to string, cannot serialize otherwise.
                tr.location = track['trackMediaURL']
                tr.image = track['trackArt']
                tr.annotation = getDescriptionByUrl(playlist['playUserUserName'],track['trackMediaURL'])
                x.add_track(tr)
    return x



@app.route("/api/v1/collections/playlists/<string:playTitle>.xspf", methods = ['GET'])
def generate_xspf(playTitle):
    try:
        key = playTitle
        key = key.replace(" ", "_")
        playlistURL = "http://localhost:8000/api/v1/collections/playlists/" + playTitle
        cache = client.get(key)
        if cache is None:
            cacheList=[]
            results = requests.get(playlistURL).json()
            playlist = results[0]
            tracks = requests.get("http://localhost:8000/api/v1/collections/tracks/all").json()
            if playlist == {'message': 'This resource does not exist.'}:
                raise exceptions.NotFound
            if tracks == {'message': 'This resource does not exist.'}:
                raise exceptions.NotFound
            tracklist = getPlayListURLs(playlist)
            cacheList.append(tracklist)
            cacheList.append(tracks)
            cacheList.append(playlist)
            client.set(key, cacheList, expire=60)
            xspf_playlist = getTrackInfoFromURL(tracklist, tracks, playlist)
        else:
            tracklist = cache[0]
            tracks = cache[1]
            playlist = cache[2]
            xspf_playlist = getTrackInfoFromURL(tracklist, tracks, playlist)
        return xspf_playlist.toXml(), status.HTTP_200_OK
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND

# if __name__ =="__main__":
#     playTitle = "Playlist 00"
#     generate_xspf(playTitle)