-- :name user_by_username :one
SELECT userID, userName, userUsername, userEmail FROM users
WHERE userUserName = :username;
