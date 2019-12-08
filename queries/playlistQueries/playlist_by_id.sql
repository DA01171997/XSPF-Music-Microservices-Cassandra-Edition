-- :name playlist_by_id :one
SELECT * FROM playlists WHERE playID = :playID;
