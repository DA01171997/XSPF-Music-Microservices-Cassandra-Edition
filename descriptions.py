import sys
import flask_api
import pugsql
from flask import request, jsonify, Response
from flask_api import status, exceptions

app = flask_api.FlaskAPI(__name__,static_url_path='')
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/descriptionQueries/')
queries.connect(app.config['DATABASE_URL'])

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
		return create_description()

def create_description():
	description = request.data
	required_fields = ['trackTitle','descriptionDesc','trackMediaURL','userUserName']
	if not all([field in description for field in required_fields]):
		raise exceptions.ParseError()
	try:
		description['descriptionID'] = queries.create_description(**description)
	except Exception as e:
		return { 'Error': str(e) }, status.HTTP_409_CONFLICT
	return description, status.HTTP_201_CREATED

#route to GET user descriptions of a track using url
@app.route('/api/v1/descriptions/users/<string:username>/descriptions', methods=['GET'])
def user_description(username):
	if request.method =='GET':
		return filter_descriptions(request.args)

def filter_descriptions(query_parameters):
	trackMediaURL = query_parameters.get('trackMediaURL')
	query = "SELECT * FROM descriptions WHERE"
	to_filter = []
	if trackMediaURL:
		query += ' trackMediaURL=? AND'
		to_filter.append(trackMediaURL)
	if not (trackMediaURL):
		raise exceptions.NotFound()
	query = query[:-4] + ';'
	results = queries._engine.execute(query, to_filter).fetchall()
	data = list(map(dict, results))
	if data:
			return data, status.HTTP_200_OK
	return { 'Error': str("Not Found") }, status.HTTP_404_NOT_FOUND

#route to GET user all  by user
@app.route('/api/v1/descriptions/users/<string:username>/descriptions/all', methods=['GET'])
def user_description_all(username):
	if request.method =='GET':
		userUserName = username
		all_description= queries.description_all(userUserName=userUserName)
		data = list(all_description)
		if data:
			return data, status.HTTP_200_OK
		return { 'Error': str("Not Found") }, status.HTTP_404_NOT_FOUND