import sys
import flask_api
import pugsql
from flask import request, jsonify, Response
from flask_api import status, exceptions

from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
#session.set_keyspace('music')


app = flask_api.FlaskAPI(__name__,static_url_path='')
app.config.from_envvar('APP_CONFIG')

def checkForKeyspace():
    if 'music' not in cluster.metadata.keyspaces:
        return {"Error" : "KEYSPACE NOT FOUND"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return True

#used to check if POST request header is application/json
def validContentType(request, type='application/json'):
    if request.headers.has_key('Content-Type'):
        if request.headers['Content-Type'] == type:
            return True
    return { 'Error':'Unsupported Media Type', 'Support-Content-Type':type}, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

#route home
@app.route('/', methods=['GET'])
def home():
	return '''<h1>description-SERVICE</h1>'''

#route to create description
@app.route('/api/v1/descriptions/', methods=['POST'])
def description():
	if request.method=='POST':
		checker = checkForKeyspace()
		if checker is not True:
			return checker
		else:
			session.set_keyspace('music')
		return create_description()

def create_description():
	description = request.data
	required_fields = ['trackTitle','descriptionDesc','trackMediaURL','userUserName']
	if not all([field in description for field in required_fields]):
		raise exceptions.ParseError()
	try:
		insert_description_cql = "INSERT INTO music.descriptions (trackTitle,descriptionDesc,trackMediaURL,userUserName) VALUES ('{}','{}','{}', '{}')".format(description['trackTitle'],description['descriptionDesc'],description['trackMediaURL'],description['userUserName'])
		session.execute(insert_description_cql)
	except Exception as e:
		return { 'Error': str(e) }, status.HTTP_409_CONFLICT
	return description, status.HTTP_201_CREATED

#route to GET user descriptions of a track using url
@app.route('/api/v1/descriptions/users/<string:username>/descriptions', methods=['GET'])
def user_description(username):
	if request.method =='GET':
		checker = checkForKeyspace()
		if checker is not True:
			return checker
		else:
			session.set_keyspace('music')
		return filter_descriptions(request.args, username)

def filter_descriptions(query_parameters, username):
	trackMediaURL = query_parameters.get('trackMediaURL')
	result = []
	data={}
	count = 0
	if trackMediaURL:
		select_description_cql = "SELECT * FROM music.descriptions WHERE trackMediaURL='{}' AND userUserName='{}'".format(trackMediaURL,username)
		rows = session.execute(select_description_cql)
		for row in rows:
			data['trackTitle'] = row.tracktitle
			data['descriptionDesc'] = row.descriptiondesc
			data['trackMediaURL'] = row.trackmediaurl
			data['userUserName'] = row.userusername
			count+=1
			result.append(data)
		if count==0:
			return { 'Error': str("Not Found") }, status.HTTP_404_NOT_FOUND
		if count>0:
			return result, status.HTTP_200_OK
	return { 'Error': str("BAD Request") }, status.HTTP_400_BAD_REQUEST
