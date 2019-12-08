
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
