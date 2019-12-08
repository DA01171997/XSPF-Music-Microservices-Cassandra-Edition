BEGIN TRANSACTION;

DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
	trackID GUID primary key,
	trackTitle TEXT NOT NULL,
	trackAlbum TEXT NOT NULL,
	trackArtist TEXT NOT NULL,
	trackLength INT NOT NULL,
	trackMediaURL TEXT NOT NULL,
	trackArt TEXT,
	UNIQUE(trackMediaURL)
);

COMMIT;