
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
    descriptionDesc map<text,text>,
    PRIMARY KEY ((trackTitle,trackArtist))
);

CREATE TABLE descriptions (
    descriptionDesc text,
    trackTitle text,
    userUserName text,
    trackMediaURL text,
    PRIMARY KEY (trackMediaURL, userUserName)
);