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
# select_all_playlist_cql = "SELECT * FROM music.playlists"
# rows = session.execute(select_all_playlist_cql)
# result = []
# data = {}
# print (str(rows))
# for row in rows:
#     data['playTitle'] = row.playtitle
#     data['playUserUserName'] = row.playuserusername
#     data['playDesc'] = row.playdesc
#     data['playListOfTracks'] = row.playlistoftracks
#     print(data)
#     result.append(data)
# {
# 	"trackTitle" : "Track title 00",
# 	"trackAlbum" : "The 00 album",
# 	"trackArtist" : "The 00 artist",
# 	"trackLength" : "120",
# 	"trackMediaURL" : "http://localhost:8000/media/song00.mp3",
# 	"trackArt" : "file:///music/art/ablum/00"
# }
# data = {}
# data['trackTitle']= "Track title 00"
# data['trackAlbum']= "The 00 album"
# data['trackArtist']= "The 00 artist"
# data['trackLength']= "120"
# data['trackMediaURL']= "http://localhost:8000/media/song00.mp3"
# data['trackArt']= "file:///music/art/ablum/00"

# insert_track_cql = "INSERT INTO tracks (trackTitle,trackAlbum,trackArtist,trackLength,trackMediaURL,trackArt) VALUES ('{}','{}','{}','{}','{}','{}')".format(data['trackTitle'],data['trackAlbum'],data['trackArtist'],data['trackLength'],data['trackMediaURL'],data['trackArt']) 
# session.execute(insert_track_cql)
track= {}
track['trackTitle']= "Track title 00"
track['trackAlbum']= "The 001 album"
track['trackArtist']= "The 00 artist"
track['trackLength']= "120"
track['trackMediaURL']= "http://localhost:8000/media/song00.mp3"
track['trackArt']= "file:///music/art/ablum/00"




# insert_track_cql = "INSERT INTO tracks (trackTitle,trackAlbum,trackArtist,trackLength,trackMediaURL,trackArt) VALUES ('{}','{}','{}','{}','{}','{}')".format(data['trackTitle'],data['trackAlbum'],data['trackArtist'],data['trackLength'],data['trackMediaURL'],data['trackArt']) 
# session.execute(insert_track_cql)

# select_track_with = "SELECT * FROM music.tracks WHERE trackTitle='{}' AND trackArtist = '{}' ".format(track["trackTitle"],track["trackArtist"])
# rows = session.execute(select_track_with)
# count = 0
# for row in rows:
#     count+=1
# if count==1:
#     insert_track_cql = "INSERT INTO tracks (trackTitle,trackAlbum,trackArtist,trackLength,trackMediaURL,trackArt) VALUES ('{}','{}','{}',{},'{}','{}')".format(track['trackTitle'],track['trackAlbum'],track['trackArtist'],track['trackLength'],track['trackMediaURL'],track['trackArt']) 
#     session.execute(insert_track_cql)
#     print("fix")
#     # return { 'Message':'DELETE REQUEST ACCEPTED - BUT NOT GUARENTEED IN EVENTUAL CONSISTENT DB'}, status.HTTP_202_ACCEPTED
# elif count==0:
#     # return { 'Error': "Playlist Doesn't Exists" }, status.HTTP_404_NOT_FOUND
#     print("doesnot exist")

select_all_track_cql = "SELECT * FROM music.tracks WHERE trackTitle='{}' AND trackArtist= '{}'".format(track['trackTitle'],track['trackArtist'])
rows = session.execute(select_all_track_cql)
count = 0
for row in rows:
    count+=1
if count==1:
    delete_track = "DELETE FROM music.tracks WHERE trackTitle='{}' AND trackArtist= '{}'".format(track['trackTitle'],track['trackArtist'])
    session.execute(delete_track)
    print("DELTE")
    # return { 'Message':'DELETE REQUEST ACCEPTED - BUT NOT GUARENTEED RIGHT NOW IN EVENTUAL CONSISTENT DB' }, status.HTTP_202_ACCEPTED  
if count==0:
    print("NOPE")
    # return { 'Error': "TRACK NOT FOUND" },status.HTTP_404_NOT_FOUND