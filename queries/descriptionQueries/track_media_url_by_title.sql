-- :name track_media_url_by_title :one
SELECT trackMediaURL FROM tracks WHERE trackTitle = :trackTitle;