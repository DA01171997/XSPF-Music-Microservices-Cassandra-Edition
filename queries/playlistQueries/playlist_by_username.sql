-- :name playlist_by_username :many
SELECT P.playID, P.playTitle, P.playDesc, P.playListOfTracks, U.userUserName 
FROM playlists as P, users as U 
WHERE U.userUserName = :userUserName AND P.playUserID = U.userID;
