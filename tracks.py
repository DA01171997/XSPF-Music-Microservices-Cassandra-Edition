import sys
from flask import request
import flask_api
from flask_api import status, exceptions
import pugsql
import sqlite3
import uuid

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar("APP_CONFIG")

if sys.version_info > (3,):
    buffer = memoryview

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le))

trackQueries = pugsql.module("queries/trackQueries/")
trackQueries.connect(app.config["DATABASE_URL"].format(stuff=sqlite3.PARSE_DECLTYPES))

trackQueries2 = pugsql.module("queries/trackQueries2/")
trackQueries2.connect(app.config["DATABASE_URL_2"].format(stuff=sqlite3.PARSE_DECLTYPES))

trackQueries3 = pugsql.module("queries/trackQueries3/")
trackQueries3.connect(app.config["DATABASE_URL_3"].format(stuff=sqlite3.PARSE_DECLTYPES))

def validContentType(request, type='application/json'):
    if request.headers.has_key('Content-Type'):
        if request.headers['Content-Type'] == type:
            return True
    return { 'Error':'Unsupported Media Type', 'Support-Content-Type':type}, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

@app.route('/api/v1/', methods=['GET'])
def home():
	return "<h1>Music Collection<h1><p>This site is a prototype API for your music collection.</p><p>This is the track handler.</p>"
    
@app.route("/api/v1/collections/tracks/all", methods = ["GET"])
def allTracks():
    allTracksFrom1 = trackQueries.all_tracks()
    allTracksFrom2 = trackQueries2.all_tracks()
    allTracksFrom3 = trackQueries3.all_tracks()
    allTracks = list(allTracksFrom1) + list(allTracksFrom2) + list(allTracksFrom3)
    if len(allTracks) is 0:
        raise exceptions.NotFound()
    else:
        return list(allTracks)

@app.route("/api/v1/collections/tracks/<uuid:trackID>", methods = ["GET", "DELETE"])
def filterTrackByID(trackID):
    shardKey = trackID.int % 3
    if request.method == "GET":
        if shardKey == 0:
            trackByID = trackQueries.track_by_id(trackID=trackID)
        elif shardKey == 1:
            trackByID = trackQueries2.track_by_id(trackID=trackID)
        elif shardKey == 2:
            trackByID = trackQueries.track_by_id(trackID=trackID)
        else:
            raise exceptions.ParseError()
        if trackByID is None:
            raise exceptions.NotFound()
        return trackByID
    elif request.method == "DELETE":
        try:
            if shardKey == 0:
                affected = trackQueries.delete_by_id(trackID = trackID)
            elif shardKey == 1:
                affected = trackQueries2.delete_by_id(trackID = trackID)
            elif shardKey == 2:
                affected = trackQueries3.delete_by_id(trackID = trackID)
            else:
                raise exceptions.ParseError()
            if affected == 0:
                return { 'Error': "TRACK NOT FOUND" },status.HTTP_404_NOT_FOUND
            else:
                return { 'DELETE REQUEST ACCEPTED': str(trackID) }, status.HTTP_202_ACCEPTED               
        except Exception as e:
            return { 'Error': str(e) }, status.HTTP_409_CONFLICT


        
@app.route('/api/v1/collections/tracks', methods=['GET', 'POST', 'PATCH'])
def tracks():
    if request.method == 'GET':
        results = filterTracks(request.args)
        if len(results) is 0:
            raise exceptions.NotFound()
        else:
            return results
    elif request.method == 'POST':
        valid = validContentType(request)
        if valid is not True:
            return valid
        return createTrack(request.data)
    elif request.method == 'PATCH':
        valid = validContentType(request)
        if valid is not True:
            return valid
        return editTrack(request.data)
    

def createTrack(track):
    track = request.data
    requiredFields = ["trackTitle", "trackAlbum", "trackArtist", "trackLength", "trackMediaURL"]
    
    if not all([field in track for field in requiredFields]):
        raise exceptions.ParseError()
    if "trackArt" not in track:
        track["trackArt"] = ""
    try:
        uniqueID = uuid.uuid4()
        shardKey = uniqueID.int % 3
        if shardKey == 0:
            track['trackID'] = uniqueID
            trackQueries.create_track(**track)
        elif shardKey == 1:
            track['trackID'] = uniqueID
            trackQueries2.create_track(**track)
        elif shardKey == 2:
            track['trackID'] = uniqueID
            trackQueries3.create_track(**track)
        else:
            raise exceptions.ParseError()
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return track, status.HTTP_201_CREATED
    
def editTrack(track):
    track = request.data
    requiredFields = ["trackID", "trackTitle", "trackAlbum", "trackArtist", "trackLength", "trackMediaURL", "trackArt"]
    if not all([field in track for field in requiredFields]):
        raise exceptions.ParseError()
    else:
        try:
            track["trackID"] = uuid.UUID(track["trackID"])
            shardKey = track["trackID"].int % 3
            if shardKey == 0:
                affected = trackQueries.edit_track(**track)
            elif shardKey == 1:
                affected = trackQueries2.edit_track(**track)
            elif shardKey == 2:
                affected = trackQueries3.edit_track(**track)
            else:
                raise exceptions.ParseError()
            
            if affected is 0:
                raise exceptions.ParseError("Update Failed")
            else:
                result = trackQueries.track_by_id(**track)
                return result, status.HTTP_200_OK
        except Exception as e:
            return {'error':str(e)}, status.HTTP_409_CONFLICT
    
def filterTracks(queryParams):
    trackTitle = queryParams.get("trackTitle")
    trackAlbum = queryParams.get("trackAlbum")
    trackArtist = queryParams.get("trackArtist")
    
    query = "SELECT * FROM tracks WHERE"
    to_filter = []
    
    if trackTitle:
        query += ' trackTitle=? AND'
        to_filter.append(trackTitle)
    if trackAlbum:
        query += ' trackAlbum=? AND'
        to_filter.append(trackAlbum)
    if trackArtist:
        query += ' trackArtist=? AND'
        to_filter.append(trackArtist)
    if not (trackTitle or trackAlbum or trackArtist):
        raise exceptions.NotFound()
        
    query = query[:-4] + ';'

    results1 = trackQueries._engine.execute(query, to_filter).fetchall()
    results2 = trackQueries2._engine.execute(query, to_filter).fetchall()
    results3 = trackQueries3._engine.execute(query, to_filter).fetchall()

    return list(map(dict, results1)) + list(map(dict, results2)) + list(map(dict, results3))