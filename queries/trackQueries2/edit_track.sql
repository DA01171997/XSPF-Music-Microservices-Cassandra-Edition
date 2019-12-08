-- :name edit_track :affected
UPDATE tracks 
SET  trackTitle = :trackTitle, trackAlbum = :trackAlbum, trackArtist = :trackArtist, trackLength = :trackLength, trackMediaURL = :trackMediaURL, trackArt = :trackArt
WHERE trackID = :trackID;