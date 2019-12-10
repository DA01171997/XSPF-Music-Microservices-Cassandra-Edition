from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()
session.set_keyspace('music')



# # cql = "Select * from music.users;"
# description = {}
# description['trackTitle'] = "Track title 00"
# description['descriptionDesc'] = "Just a descripton of my track"
# description['trackMediaURL'] = "http://localhost:8000/media/song00.mp3"
# description['userUserName'] = "WassupMan404"
# cql = "INSERT INTO music.descriptions (trackTitle,descriptionDesc,trackMediaURL','userUserName') VALUES ('{}','{}','{}', '{}')".format(description['trackTitle'],description['descriptionDesc'],description['trackMediaURL'],description['userUserName'])
# cql="SELECT * FROM music.descriptions WHERE trackMediaURL='{}' AND userUserName='{}'".format('http://localhost:8000/media/song00.mp3','WassupMan404')
# templist = ["http://localhost:8000/media/song00.mp3", "http://localhost:8000/media/song01.mp3", "http://localhost:8000/media/song02.mp3", "http://localhost:8000/media/song03.mp3", "http://localhost:8000/media/song05.mp3", "http://localhost:8000/media/song10.mp3"]
# cql  = "INSERT INTO music.playlists (playTitle,playUserUserName,playListOfTracks,playDesc) VALUES ('kljlk','dfdfd',{},'s')".format(list(templist))
# {
# 	"playTitle" : "Playlist 02",
# 	"playUserUserName": 2,
# 	"playDesc" : "This is my playlist for bad music.",
# 	"playListOfTracks" : ["http://localhost:8000/media/song02.mp3", "http://localhost:8000/media/song05.mp3", "http://localhost:8000/media/song09.mp3"]
# }
# playlist={}
# playlist['playTitle'] = "Playlist 02"
# playlist['playUserUserName'] = "2"
# tempList = ["http://localhost:8000/media/song02.mp3", "http://localhost:8000/media/song05.mp3", "http://localhost:8000/media/song09.mp3"]
# playlist['playDesc'] = "This is my playlist for bad music."

# insert_playlist_cql = "INSERT INTO music.playlists (playTitle,playUserUserName,playListOfTracks,playDesc) VALUES ('{}','{}',{},'{}')".format(playlist['playTitle'],playlist['playUserUserName'],list(tempList),playlist['playDesc'])
# session.execute(insert_playlist_cql)
select_all_playlist_cql = "SELECT * FROM music.playlists"
rows = session.execute(select_all_playlist_cql)
result = []
data = {}
print (str(rows))
for row in rows:
    data['playTitle'] = row.playtitle
    data['playUserUserName'] = row.playuserusername
    data['playDesc'] = row.playdesc
    data['playListOfTracks'] = row.playlistoftracks
    print(data)
    result.append(data)