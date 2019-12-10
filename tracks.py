import sys
from flask import request
import flask_api
from flask_api import status, exceptions
import pugsql
import sqlite3
import uuid

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
	return "<h1>Music Collection<h1><p>This site is a prototype API for your music collection.</p><p>This is the track handler.</p>"
    
@app.route("/api/v1/collections/tracks/all", methods = ["GET"])
def allTracks():
    try:
        select_all_track_cql = "SELECT * FROM music.tracks"
        rows = session.execute(select_all_track_cql)
        result = []
        for row in rows:
            data = {}
            data['trackTitle'] = row.tracktitle
            data['trackAlbum'] = row.trackalbum
            data['trackArtist'] = row.trackartist
            data['trackLength'] = row.tracklength
            data['trackMediaURL'] = row.trackmediaurl
            data['trackArt'] = row.trackart
            result.append(data)
        if result:
            return result, status.HTTP_200_OK
        return { 'Error': "Not Found" }, status.HTTP_404_NOT_FOUND
    except Exception as e:
            return { 'Error': str(e) }, status.HTTP_409_CONFLICT

@app.route("/api/v1/collections/tracks/<string:trackTitle>/<string:trackArtist>", methods = ["GET", "DELETE"])
def filterTrackByID(trackTitle,trackArtist):
    if request.method == "GET":
        try:
            select_all_track_cql = "SELECT * FROM music.tracks WHERE trackTitle='{}' AND trackArtist= '{}'".format(trackTitle,trackArtist)
            rows = session.execute(select_all_track_cql)
            for row in rows:
                data = {}
                data['trackTitle'] = row.tracktitle
                data['trackAlbum'] = row.trackalbum
                data['trackArtist'] = row.trackartist
                data['trackLength'] = row.tracklength
                data['trackMediaURL'] = row.trackmediaurl
                data['trackArt'] = row.trackart
            if data:
                return data, status.HTTP_200_OK
            else:
                return { 'Error': "Not Found" }, status.HTTP_404_NOT_FOUND
        except Exception as e:
            return { 'Error': str(e) }, status.HTTP_409_CONFLICT
        return { 'Error': "Not Found" }, status.HTTP_404_NOT_FOUND
    elif request.method == "DELETE":
        try:
            select_all_track_cql = "SELECT * FROM music.tracks WHERE trackTitle='{}' AND trackArtist= '{}'".format(trackTitle,trackArtist)
            rows = session.execute(select_all_track_cql)
            count = 0
            for row in rows:
                count+=1
            if count==1:
                delete_track = "DELETE FROM music.tracks WHERE trackTitle='{}' AND trackArtist= '{}'".format(trackTitle,trackArtist)
                session.execute(delete_track)
                return { 'Message':'DELETE REQUEST ACCEPTED - BUT NOT GUARENTEED RIGHT NOW IN EVENTUAL CONSISTENT DB' }, status.HTTP_202_ACCEPTED  
            if count==0:
                return { 'Error': "TRACK NOT FOUND" },status.HTTP_404_NOT_FOUND
        except Exception as e:
            return { 'Error': str(e) }, status.HTTP_409_CONFLICT


        
@app.route('/api/v1/collections/tracks', methods=['GET','POST', 'PATCH'])
def tracks():
    if request.method == 'GET':
        results = filterTracks(request.args)
        if len(results) is 0:
            return { 'Error': str("Not Found") }, status.HTTP_404_NOT_FOUND
        else:
            return results
    if request.method == 'POST':
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
        count =0
        insert_track_cql = "INSERT INTO tracks (trackTitle,trackAlbum,trackArtist,trackLength,trackMediaURL,trackArt) VALUES ('{}','{}','{}',{},'{}','{}')".format(track['trackTitle'],track['trackAlbum'],track['trackArtist'],track['trackLength'],track['trackMediaURL'],track['trackArt']) 
        session.execute(insert_track_cql)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    return track, status.HTTP_201_CREATED
    
def editTrack(track):
    track = request.data
    requiredFields = ["trackTitle", "trackAlbum", "trackArtist", "trackLength", "trackMediaURL"]
    if not all([field in track for field in requiredFields]):
        raise exceptions.ParseError()
    if "trackArt" not in track:
        track["trackArt"] = ""
    try:
        select_track_with = "SELECT * FROM music.tracks WHERE trackTitle='{}' AND trackArtist = '{}' ".format(track["trackTitle"],track["trackArtist"])
        rows = session.execute(select_track_with)
        count = 0
        for row in rows:
            count+=1
        if count==1:
            insert_track_cql = "INSERT INTO tracks (trackTitle,trackAlbum,trackArtist,trackLength,trackMediaURL,trackArt) VALUES ('{}','{}','{}',{},'{}','{}')".format(track['trackTitle'],track['trackAlbum'],track['trackArtist'],track['trackLength'],track['trackMediaURL'],track['trackArt']) 
            session.execute(insert_track_cql)
            return track, status.HTTP_200_OK
        elif count==0:
            return { 'Error': "Track Doesn't Exists" }, status.HTTP_404_NOT_FOUND
    except Exception as e:
        return {'error':str(e)}, status.HTTP_409_CONFLICT
    return track, status.HTTP_200_OK


def filterTracks(query_parameters):
    trackMediaURL = query_parameters.get('trackMediaURL')
    result = []
    count = 0
    if trackMediaURL:
        select_track_cql = "SELECT * FROM music.tracks WHERE trackMediaURL='{}'".format(trackMediaURL)
        rows = session.execute(select_track_cql)
        for row in rows:
            data = {}
            data['trackTitle'] = row.tracktitle
            data['trackAlbum'] = row.trackalbum
            data['trackArtist'] = row.trackartist
            data['trackLength'] = row.tracklength
            data['trackMediaURL'] = row.trackmediaurl
            data['trackArt'] = row.trackart
            count+=1
            result.append(data)
        if count==0:
            return { 'Error': str("Not Found") }, status.HTTP_404_NOT_FOUND
        if count>0:
            return result, status.HTTP_200_OK
    return { 'Error': str("BAD Request") }, status.HTTP_400_BAD_REQUEST