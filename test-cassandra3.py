from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('music')



# cql = "Select * from music.users;"
description = {}
description['trackTitle'] = "Track title 00"
description['descriptionDesc'] = "Just a descripton of my track"
description['trackMediaURL'] = "http://localhost:8000/media/song00.mp3"
description['userUserName'] = "WassupMan404"
cql = "INSERT INTO music.descriptions (trackTitle,descriptionDesc,trackMediaURL','userUserName') VALUES ('{}','{}','{}', '{}')".format(description['trackTitle'],description['descriptionDesc'],description['trackMediaURL'],description['userUserName'])
session.execute(cql)
