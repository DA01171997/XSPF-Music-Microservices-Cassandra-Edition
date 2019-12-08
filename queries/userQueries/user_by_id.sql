-- :name user_by_id :one
SELECT userID, userName, userUsername, userEmail FROM users
WHERE userID = :id;
