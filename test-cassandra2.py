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
# cql = "SELECT * FROM users;"
# print(userPassword)

# print(cql)

# count = 0
# result = []
# for row in rows:
#     data = {}
#     data['userName'] = row.username
#     data['userUserName'] = row.userusername
#     data['userEmail'] = row.useremail
#     result.append(data)

# print(count)
# print(result)
cql = "UPDATE music.users SET userpassword='11223' WHERE userUserName='unitTestUser';"
rows = session.execute(cql)
