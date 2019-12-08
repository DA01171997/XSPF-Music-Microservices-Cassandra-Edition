import json, requests
from xspf import xspf
from flask import request, jsonify, Response
import flask_api
from flask_api import status, exceptions
import xml.dom.minidom
from requests.exceptions import HTTPError

app = flask_api.FlaskAPI(__name__,static_url_path='')

def getPlayListByID(id, playlists):
    for playlist in playlists:
        if playlist['playID'] == id:
            return playlist

def getUserByID(id):
    userstr = "http://localhost:8000/api/v1/users/id/%d" % (id)
    user = requests.get(userstr).json()
    return user

def getDescriptionByUser(uid):
    descstr = "http://localhost:8000/api/v1/descriptions/users/%s/descriptions/all" % (uid)
    desc = requests.get(descstr).json()
    return desc

def getPlayListURLs(playlist):
    urls = playlist['playListOfTracks'].strip('[]').split(',')
    playlist_urls = []
    for url in urls:
        playlist_urls.append(url.strip(' ').strip('\''))
    return playlist_urls

def getTrackInfoFromURL(urls, tracks, playlist):
    x = xspf.Xspf()
    x.title = playlist['playTitle']

    user = getUserByID(playlist['playUserID'])

    x.creator = user['userUserName']

    desc = getDescriptionByUser(user['userUserName'])
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
                if track['trackMediaURL'] == desc[0]['trackMediaURL']:
                    tr.annotation = desc[0]['descriptionDesc']
                x.add_track(tr)
    return x

@app.route("/api/v1/collections/playlists/<int:playID>.xspf", methods = ['GET'])
def generate_xspf(playID):
        playlistURL = "http://localhost:8000/api/v1/collections/playlists/" + str(playID)
        playlist = requests.get(playlistURL).json()
        tracks = requests.get("http://localhost:8000/api/v1/collections/tracks/all").json()
        if playlist == {'message': 'This resource does not exist.'}:
            raise exceptions.NotFound
        if tracks == {'message': 'This resource does not exist.'}:
            raise exceptions.NotFound
        tracklist = getPlayListURLs(playlist)
        xspf_playlist = getTrackInfoFromURL(tracklist, tracks, playlist)
        return xspf_playlist.toXml(), status.HTTP_200_OK
