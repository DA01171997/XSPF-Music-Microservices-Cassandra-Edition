import sys
from flask import request, jsonify
import flask_api
from flask_api import status, exceptions
import pugsql

from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('music')

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar("APP_CONFIG")

def validContentType(request, type='application/json'):
    if request.headers.has_key('Content-Type'):
        if request.headers['Content-Type'] == type:
            return True
    return { 'Error':'Unsupported Media Type', 'Support-Content-Type':type}, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

@app.route('/api/v1/', methods=['GET'])
def home():
	return "<h1>Music Collection<h1><p>This site is a prototype API for your music collection.</p><p>This is the playlist handler.</p>"
    
@app.route("/api/v1/collections/playlists/all", methods = ["GET"])
def allPlaylists():
    select_all_playlist_cql = "SELECT * FROM music.playlists"
    rows = session.execute(select_all_playlist_cql)
    result = []
    for row in rows:
        data = {}
        data['playTitle'] = row.playtitle
        data['playUserUserName'] = row.playuserusername
        data['playDesc'] = row.playdesc
        data['playListOfTracks'] = row.playlistoftracks
        result.append(data)
    if result:
        return result, status.HTTP_200_OK
    return { 'Error': "Not Found" }, status.HTTP_404_NOT_FOUND
        

@app.route("/api/v1/collections/playlists/<string:playTitle>", methods = ["GET", "DELETE"])
def filterPlaylistsByID(playTitle):
    if request.method == "GET":
        select_playlist_withTitle_cql = "SELECT * FROM music.playlists WHERE playTitle='{}'".format(playTitle)
        rows = session.execute(select_playlist_withTitle_cql)
        result = []
        for row in rows:
            data = {}
            data['playTitle'] = row.playtitle
            data['playUserUserName'] = row.playuserusername
            data['playDesc'] = row.playdesc
            data['playListOfTracks'] = row.playlistoftracks
            result.append(data)
        if result:
            return result, status.HTTP_200_OK
        return { 'Error': "Not Found" }, status.HTTP_404_NOT_FOUND
    elif request.method == "DELETE":
        try:
            select_all_playlist_cql = "SELECT * FROM music.playlists WHERE playTitle='{}'".format(playTitle)
            rows = session.execute(select_all_playlist_cql)
            count = 0
            for row in rows:
                count+=1
            if count==1:
                delete_playlist_cql = "DELETE FROM music.playlists WHERE playTitle = '{}'".format(playTitle)
                session.execute(delete_playlist_cql)
                return { 'Message':'DELETE REQUEST ACCEPTED - BUT NOT GUARENTEED IN EVENTUAL CONSISTENT DB'}, status.HTTP_202_ACCEPTED
            elif count==0:
                return { 'Error': "Playlist Doesn't Exists" }, status.HTTP_404_NOT_FOUND
        except Exception as e:
            return { 'Error': str(e) }, status.HTTP_409_CONFLICT
        return { 'Error': str(e) }, status.HTTP_409_CONFLICT

    
@app.route("/api/v1/collections/playlists/users/<string:username>/playlists", methods = ["GET"])
def playlistByUsername(username):
    if request.method == "GET":
        select_all_playlist_by_user_cql = "SELECT * FROM music.playlists WHERE playUserUserName='{}'".format(username)
        rows = session.execute(select_all_playlist_by_user_cql)
        result = []
        for row in rows:
            data = {}
            data['playTitle'] = row.playtitle
            data['playUserUserName'] = row.playuserusername
            data['playDesc'] = row.playdesc
            data['playListOfTracks'] = row.playlistoftracks
            result.append(data)
        if result:
            return result, status.HTTP_200_OK
        return { 'Error': "Not Found" }, status.HTTP_404_NOT_FOUND
        
    
@app.route('/api/v1/collections/playlists', methods=['POST'])
def playlists():
    if request.method == 'POST':
        valid = validContentType(request)
        if valid is not True:
            return valid
        return createPlaylist(request.data)

def createPlaylist(playlist):
    playlist = request.data
    requiredFields = ["playTitle", "playUserUserName", "playListOfTracks"]
    if not all([field in playlist for field in requiredFields]):
        raise exceptions.ParseError()
    if "playDesc" not in playlist:
        playlist["playDesc"] = ""
    try:
        tempList = list(playlist['playListOfTracks'])
        insert_playlist_cql = "INSERT INTO music.playlists (playTitle,playUserUserName,playListOfTracks,playDesc) VALUES ('{}','{}',{},'{}')".format(playlist['playTitle'],playlist['playUserUserName'],tempList,playlist['playDesc'])
        session.execute(insert_playlist_cql)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    return playlist, status.HTTP_201_CREATED
