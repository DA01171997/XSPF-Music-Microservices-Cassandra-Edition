import sys
import flask_api
import pugsql
from flask import request, jsonify, Response
from flask_api import status, exceptions
from werkzeug.security import generate_password_hash, check_password_hash
from cassandra.cluster import Cluster

cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
#session.set_keyspace('music')

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

def checkForKeyspace():
    if 'music' not in cluster.metadata.keyspaces:
        return {"Error" : "KEYSPACE NOT FOUND"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return True

def validContentType(request, type='application/json'):
    if request.headers.has_key('Content-Type'):
        if request.headers['Content-Type'] == type:
            return True
    return { 'Error':'Unsupported Media Type', 'Support-Content-Type':type}, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

@app.route('/', methods=['GET'])
def home():
    return '''<h1>USER-SERVICE</h1>'''


@app.route('/api/v1/users/register', methods=['POST', 'GET'])
def register():
    if request.method=='GET':
        try:
            checker = checkForKeyspace()
            if checker is not True:
                return checker
            else:
                session.set_keyspace('music')
            cql = "SELECT * FROM users;"
            rows = session.execute(cql)
            count = 0
            result = []
            for row in rows:
                data = {}
                data['userName'] = row.username
                data['userUserName'] = row.userusername
                data['userEmail'] = row.useremail
                result.append(data)
            return result, status.HTTP_200_OK
        except Exception as e:
            return { 'Error': str(e) }, status.HTTP_409_CONFLICT
    elif request.method=='POST':
        checker = checkForKeyspace()
        if checker is not True:
            return checker
        else:
            session.set_keyspace('music')
        valid = validContentType(request)
        if valid is not True:
            return valid
        return create_user()

def create_user():
    user = request.data
    required_fields = ['userName','userUserName','userEmail','userPassword']
    if not all([field in user for field in required_fields]):
        raise exceptions.ParseError()
    try:
        count = 0
        user['userPassword'] = generate_password_hash(user['userPassword'])
        register_cql = "INSERT INTO users (userName, userUserName, userEmail, userPassword) VALUES ('{}','{}','{}','{}')".format(user['userName'],user['userUserName'],user['userEmail'],user['userPassword'])
        check__userUserName_cql = "Select * From users WHERE userUserName='{}'".format(user['userUserName'])
        check_email_cql = "Select * From users WHERE userEmail='{}'ALLOW FILTERING ".format(user['userEmail'])
        rows = session.execute(check__userUserName_cql)
        count = 0
        for row in rows:
            count+=1
        rows = session.execute(check_email_cql)
        for row in rows:
            count+=1
        if count==0:
            session.execute(register_cql)
        else:
            return { 'Error': 'Username or Email already exists' }, status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'Error': str(e) }, status.HTTP_409_CONFLICT
    return user, status.HTTP_201_CREATED


@app.route('/api/v1/users/<string:username>', methods=['GET', 'DELETE'])
def user_username(username):
    if request.method=='GET':
        checker = checkForKeyspace()
        if checker is not True:
            return checker
        else:
            session.set_keyspace('music')
        return get_user_by_username(username)
    elif request.method=='DELETE':
        checker = checkForKeyspace()
        if checker is not True:
            return checker
        else:
            session.set_keyspace('music')
        return delete_user_by_username(username)


def get_user_by_username(username):
    try:
        get_user_cql = "SELECT * FROM users WHERE userUsername = '{}'".format(username)
        rows = session.execute(get_user_cql)
        count = 0
        for row in rows:
            data = {}
            data['userName'] = row.username
            data['userUserName'] = row.userusername
            data['userEmail'] = row.useremail
            count+=1
        if count!=0:
            return data, status.HTTP_200_OK
    except Exception as e:
        return { 'Error': str(e) }, status.HTTP_404_NOT_FOUND
    return { 'Error': "User Doesn't Exists" }, status.HTTP_404_NOT_FOUND 

def delete_user_by_username(username):
    try:
        get_user_cql = "SELECT * FROM users WHERE userUsername = '{}'".format(username)
        rows = session.execute(get_user_cql)
        count = 0
        for row in rows:
            count+=1
        if count==1:
            delete_user_cql = "DELETE FROM music.users WHERE userusername = '{}'".format(username)
            session.execute(delete_user_cql)
            return { 'Message':'DELETE REQUEST ACCEPTED - BUT NOT GUARENTEED RIGHT NOW IN EVENTUAL CONSISTENT DB'}, status.HTTP_202_ACCEPTED
        elif count==0:
            return { 'Error': "User Doesn't Exists" }, status.HTTP_404_NOT_FOUND 
    except Exception as e:
        return { 'Error': str(e) }, status.HTTP_409_CONFLICT 
    return { 'Error': str(e) }, status.HTTP_409_CONFLICT 


@app.route('/api/v1/users/login', methods=['POST'])
def login():
    if request.method=='POST':
        checker = checkForKeyspace()
        if checker is not True:
            return checker
        else:
            session.set_keyspace('music')
        valid = validContentType(request)
        if valid is not True:
            return valid
        return authenticate()
    
def authenticate():
    user = request.data
    required_fields = ['userUserName','userPassword']
    if not all([field in user for field in required_fields]):
        raise exceptions.ParseError()
    try:
        get_user_cql = "SELECT * FROM users WHERE userUsername = '{}'".format(user['userUserName'])
        rows = session.execute(get_user_cql)
        count = 0
        for row in rows:
            data = {}
            data['userName'] = row.username
            data['userUserName'] = row.userusername
            data['userEmail'] = row.useremail
            data['userPassword'] = row.userpassword
            count+=1
        if count!=0:
            if check_password_hash(data['userPassword'],user['userPassword']):
                return user, status.HTTP_200_OK
        return { 'Error': 'Login information invalid' }, status.HTTP_401_UNAUTHORIZED
    except Exception as e:
        return { 'Error': str(e) }, status.HTTP_409_CONFLICT


@app.route('/api/v1/users/<string:username>/password', methods=['PATCH'])
def password(username):
    if request.method=='PATCH':
        checker = checkForKeyspace()
        if checker is not True:
            return checker
        else:
            session.set_keyspace('music')
        valid = validContentType(request)
        if valid is not True:
            return valid
        return update_password(username)

def update_password(username):
    user = request.data
    required_fields = ['userUserName','userPassword', 'userNewPassword']
    if not all([field in user for field in required_fields]):
        raise exceptions.ParseError()
    try:
        get_user_cql = "SELECT * FROM users WHERE userUsername = '{}'".format(user['userUserName'])
        rows = session.execute(get_user_cql)
        count = 0
        for row in rows:
            data = {}
            data['userName'] = row.username
            data['userUserName'] = row.userusername
            data['userEmail'] = row.useremail
            data['userPassword'] = row.userpassword
            count+=1
        if count!=0:
            if check_password_hash(data['userPassword'],user['userPassword']):
                user['userPassword'] = generate_password_hash(user['userNewPassword'])
                cql = "UPDATE music.users SET userpassword='{}' WHERE userUserName='{}'".format(user['userPassword'], user['userUserName'])
                rows = session.execute(cql)
                return user, status.HTTP_200_OK
        return { 'Error': 'Login information invalid' }, status.HTTP_401_UNAUTHORIZED
    except Exception as e:
        return { 'Error': str(e) }, status.HTTP_409_CONFLICT
    return { 'Error': str(e) }, status.HTTP_409_CONFLICT
