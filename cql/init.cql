
DROP KEYSPACE IF EXISTS music;
CREATE KEYSPACE music
    WITH replication = {
        'class': 'SimpleStrategy',
        'replication_factor': 1
    };

Use music;
CREATE TABLE users (
    userName text,
    userUserName text,
    userEmail text,
    userPassword text,
    PRIMARY KEY(userUserName)
);

CREATE TABLE tracks (
    trackTitle text,
    trackAlbum text,
    trackArtist text,
    trackLength int,
    trackMediaURL text,
    trackArt text,
    PRIMARY KEY (trackTitle)
);

CREATE TABLE descriptions (
    descriptionDesc text,
    trackTitle text,
    userUserName text,
    trackMediaURL text,
    PRIMARY KEY (trackMediaURL, userUserName)
);

CREATE TABLE playlists (
    playTitle text,
    playUserUserName text,
    playDesc text,
    playListOfTracks list<text>,
    PRIMARY KEY (playTitle)
);

CREATE INDEX playlists_playUserUserName_index ON playlists(playUserUserName);