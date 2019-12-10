-- :name create_playlist :insert
INSERT INTO playlists(playTitle, playUserUserName, playDesc, playListOfTracks)
VALUES(:playTitle, :playUserUserName, :playDesc, :playListOfTracks)
