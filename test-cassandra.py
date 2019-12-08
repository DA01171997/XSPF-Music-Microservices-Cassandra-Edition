from cassandra.cluster import Cluster
from werkzeug.security import generate_password_hash, check_password_hash

cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('music')



# rows = session.execute('SELECT cluster_name FROM system.local')
# rows = session.execute('select * from system_schema.keyspaces')
# for row in rows:
#     print(row)


userName = str("Mr. Anderson")
userUserName ="WassupMan405"
userEmail = "neo@matrix.com"
userPassword = "123456"
userPassword = generate_password_hash(userPassword)
register_cql = "INSERT INTO users (userName, userUserName, userEmail, userPassword) VALUES ('{}','{}','{}','{}')".format(userName,userUserName,userEmail,userPassword)
check_cql_user = "Select * From users WHERE userUserName='{}'".format(userUserName)
check_cql_email = "Select * From users WHERE userEmail='{}'ALLOW FILTERING ".format(userEmail)
# print(userPassword)

# print(cql)
rows = session.execute(check_cql_user)
count = 0
for row in rows:
    count+=1
rows = session.execute(check_cql_user)
for row in rows:
    count+=1

print(count)
if count==0:
    session.execute(register_cql)
else:
    print("already exist")