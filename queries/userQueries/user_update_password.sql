-- :name user_update_password :affected
UPDATE users
SET userPassword = :userPassword
WHERE userUserName = :userUserName;