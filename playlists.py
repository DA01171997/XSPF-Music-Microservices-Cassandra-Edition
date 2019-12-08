import sys
from flask import request, jsonify
import flask_api
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar("APP_CONFIG")

plQueries = pugsql.module("queries/playlistQueries/")
plQueries.connect(app.config["DATABASE_URL"])

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
    allPlaylists = plQueries.all_playlists()
    allPlaylists = list(allPlaylists)
    if len(allPlaylists) is 0:
        raise exceptions.NotFound()
    else:
        return allPlaylists

@app.route("/api/v1/collections/playlists/<int:playID>", methods = ["GET", "DELETE"])
def filterPlaylistsByID(playID):
    if request.method == "GET":
        playlistByID = plQueries.playlist_by_id(playID=playID)
        if playlistByID is None:
           raise exceptions.NotFound()
        else:
            return playlistByID
    elif request.method == "DELETE":
        try:
            affected = plQueries.delete_by_id(playID = playID)
            trackListPlayID = playID
            affected2 = plQueries.delete_from_trackLists(trackListPlayID = trackListPlayID)
            if affected == 0 or affected2 == 0:
                return { 'Error': "PLAYLIST NOT FOUND" },status.HTTP_404_NOT_FOUND
            else:
                return { 'DELETE REQUEST ACCEPTED': str(playID) }, status.HTTP_202_ACCEPTED               
        except Exception as e:
            return { 'Error': str(e) }, status.HTTP_409_CONFLICT


    
@app.route("/api/v1/collections/playlists/users/<string:username>/playlists", methods = ["GET"])
def playlistByUsername(username):
    if request.method == "GET":
        userUserName = username
        stuff = plQueries.playlist_by_username(userUserName = userUserName)
        data = list(stuff)
        if data:
            return data
        return { 'Error': "Not Found" }, status.HTTP_404_NOT_FOUND
        
    
@app.route('/api/v1/collections/playlists', methods=['GET', 'POST'])
def playlists():
    if request.method == 'GET':
        results = filterPlaylists(request.args)
        if len(results) is 0:
            raise exceptions.NotFound()
        else:
            return results
    elif request.method == 'POST':
        valid = validContentType(request)
        if valid is not True:
            return valid
        return createPlaylist(request.data)

def createPlaylist(playlist):
    playlist = request.data
    requiredFields = ["playTitle", "playUserID", "playListOfTracks"]
    if not all([field in playlist for field in requiredFields]):
        raise exceptions.ParseError()
    if "playDesc" not in playlist:
        playlist["playDesc"] = ""
    try:
        tempList = list(playlist['playListOfTracks'])
        playlist['playListOfTracks'] = str(playlist['playListOfTracks'])
        playlist['playID'] = plQueries.create_playlist(**playlist)
        listOfTracks = []
        for track in tempList:
            listOfTracks.append(track)
        for track in listOfTracks:
            TrackURLID=plQueries.add_to_trackList(trackListPlayID=playlist['playID'], trackListURL = track)
            if not TrackURLID:
                raise exceptions.ParseError()
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    return playlist, status.HTTP_201_CREATED
    
def filterPlaylists(queryParams):
    playID = queryParams.get("playID")
    playTitle = queryParams.get("playTitle")
    userName = queryParams.get("userName")
    
    query = "SELECT P.playID, P.playTitle, P.playDesc, P.playListOfTracks, U.userUserName FROM playlists as P, users as U WHERE P.playUserID = U.userID AND"
    to_filter = []
    
    if playID:
        query += ' P.playID=? AND'
        to_filter.append(playID)
    if playTitle:
        query += ' P.playTitle=? AND'
        to_filter.append(playTitle)
    if userName:
        query += " U.userUserName = ? AND"
        to_filter.append(userName)
    if not (playID or playTitle or userName):
        raise exceptions.NotFound()  
     
    query = query[:-4] + ';'

    results = plQueries._engine.execute(query, to_filter).fetchall()
    results = list(map(dict, results))

    return results