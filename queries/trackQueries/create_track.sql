-- :name create_track :insert
INSERT INTO tracks(trackID, trackTitle, trackAlbum, trackArtist, trackLength, trackMediaURL, trackArt)
VALUES(:trackID, :trackTitle, :trackAlbum, :trackArtist, :trackLength, :trackMediaURL, :trackArt)
