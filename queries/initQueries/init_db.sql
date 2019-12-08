BEGIN TRANSACTION;
DROP TABLE IF EXISTS playlists;
CREATE TABLE playlists (
    	playID INTEGER primary key,
    	playTitle TEXT NOT NULL,
    	playUserID INT,
    	playDesc TEXT,
	playListOfTracks TEXT NOT NULL,
	FOREIGN KEY(playUserID) REFERENCES users (userID) ON DELETE CASCADE
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
	userID INTEGER PRIMARY KEY,
	userName TEXT NOT NULL,
	userUserName TEXT NOT NULL,
	userEmail TEXT NOT NULL,
	userPassword TEXT NOT NULL,
	UNIQUE(userEmail,userUserName)
);

DROP TABLE IF EXISTS descriptions;
CREATE TABLE descriptions (
	descriptionID INTEGER PRIMARY KEY,
	descriptionDesc TEXT NOT NULL,
	trackTitle TEXT NOT NULL,
	userUserName TEXT NOT NULL,
	trackMediaURL TEXT NOT NULL,
	FOREIGN KEY(trackTitle) REFERENCES users (trackTitle) ON DELETE CASCADE,
	FOREIGN KEY(userUserName) REFERENCES tracks (userUserName) ON DELETE CASCADE,
	FOREIGN KEY(trackMediaURL) REFERENCES users (trackMediaURL) ON DELETE CASCADE
);

DROP TABLE IF EXISTS trackLists;
CREATE TABLE trackLists(
	trackListID INTEGER PRIMARY KEY,
	trackListPlayID INT,
	trackListURL TEXT,
	FOREIGN KEY(trackListPlayID) REFERENCES playlists (playID) on DELETE CASCADE,
	FOREIGN KEY(trackListURL) REFERENCES tracks (trackMediaURL) on DELETE CASCADE
);

COMMIT;
