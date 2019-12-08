-- :name create_playlist :insert
INSERT INTO playlists(playTitle, playUserID, playDesc, playListOfTracks)
VALUES(:playTitle, :playUserID, :playDesc, :playListOfTracks)
